import matplotlib.pyplot as plt
import numpy as np
import io
from io import BytesIO
import base64
from fastapi import APIRouter, File, UploadFile, HTTPException
from pydantic import BaseModel
from app.services.EmbeddingSequence import generate_vector, parse_fasta_and_filter, fasta_to_dataframe, transform_batch_3d
from app.services.igxai import draw_ig_highlight_full, compute_integrated_gradients, explain_ig_top_k
from tensorflow.keras.models import load_model
import joblib
from fastapi.responses import StreamingResponse
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm


router = APIRouter()

# Load model & scaler
scaler = joblib.load("./app/AImodel/scaler_17.save")
model = load_model("./app/AImodel/lstm_model_17.keras")

class PeptideRequest(BaseModel):
    sequence: str
@router.post("/dudoan")
async def explain_peptide(data: PeptideRequest):
    vec = generate_vector(data.sequence)
    vec_scaled = scaler.transform(vec)
    X_input = np.expand_dims(vec_scaled, axis=0)  
    y_pred = model.predict(X_input)
    prob = float(y_pred[0][0])
    label = int(prob >= 0.5)
    print(f"Predicted probability: {prob}, label: {label}")
    baseline = np.zeros_like(X_input)
    ig = compute_integrated_gradients(model, X_input, baseline=baseline)
    ig = ig.squeeze()
    top_feats = explain_ig_top_k(ig, k=4)
    fig = draw_ig_highlight_full(data.sequence, top_feats)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=150)
    plt.close(fig)
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode("utf-8")
    img_uri = f"data:image/png;base64,{img_base64}"
    return {
        "sequence": data.sequence,
        "label": label,
        "top_features": top_feats,
        "highlight_img": img_uri
    }

@router.post("/dudoan_fasta")
async def predict_fasta(file: UploadFile = File(...)):
    if not file.filename.endswith((".fasta", ".fa", ".fna")):
        raise HTTPException(status_code=400, detail="File phải có định dạng .fasta hoặc .fa")

    valid_content, skipped_content = await parse_fasta_and_filter(file)

    df = fasta_to_dataframe(valid_content)
    df_er = fasta_to_dataframe(skipped_content)

    X = np.array([generate_vector(seq) for seq in df["Sequence"]])
    X_test_scaled = transform_batch_3d(X, scaler, n_steps=7, n_features=18)
    y_pred_prob = model.predict(X_test_scaled, batch_size=128)
    y_pred_bin = (y_pred_prob > 0.5).astype("int32")


    # build DataFrame như bạn đang làm:
    df["Prediction"] = ["AMP" if int(lbl) else "nAMP" for lbl in y_pred_bin]
    df["Probability"] = [float(p) for p in y_pred_prob]

# export Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Predictions"
    for row in dataframe_to_rows(df[["ID", "Sequence", "Prediction", "Probability"]], index=False, header=True):
        ws.append(row)

    excel_io = BytesIO()
    wb.save(excel_io)
    excel_io.seek(0)

    return StreamingResponse(
    excel_io,
    media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    headers={"Content-Disposition": "attachment; filename=predictions.xlsx"}
)



@router.post("/dudoan_fasta_pdf")
async def predict_fasta_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith((".fasta", ".fa", ".fna")):
        raise HTTPException(status_code=400, detail="File phải có định dạng .fasta hoặc .fa")

    # Xử lý đầu vào
    valid_content, skipped_content = await parse_fasta_and_filter(file)
    df = fasta_to_dataframe(valid_content)
    X = np.array([generate_vector(seq) for seq in df["Sequence"]])
    X_test_scaled = transform_batch_3d(X, scaler, n_steps=7, n_features=18)
    y_pred_prob = model.predict(X_test_scaled, batch_size=128)
    y_pred_bin = (y_pred_prob > 0.5).astype("int32")

    df["Prediction"] = ["AMP" if int(lbl) else "nAMP" for lbl in y_pred_bin]
    df["Probability"] = [float(p) for p in y_pred_prob]  # giữ nguyên xác suất gốc

    # Bắt đầu render PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=2*cm,
        rightMargin=1*cm,
        topMargin=1*cm,
        bottomMargin=1*cm
    )

    styles = getSampleStyleSheet()
    elements = [
        Paragraph("📄 Peptide Prediction Report", styles['Title']),
        Spacer(1, 20)
    ]

    # Chuẩn bị dữ liệu bảng
    PAGE_WIDTH = A4[0]
    usable_width = PAGE_WIDTH - (2*cm + 1*cm)
    data = [["Sequence", "Prediction", "Probability"]] + [
        [row["Sequence"], row["Prediction"], f"{row['Probability']:.4f}"]
        for _, row in df.iterrows()
    ]

    table = Table(data, colWidths=[
        0.6 * usable_width,  # Sequence dài
        0.15 * usable_width, # Prediction ngắn
        0.25 * usable_width  # Probability vừa
    ])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E90FF")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
    ]))

    elements.append(table)
    doc.build(elements)
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "inline; filename=predictions.pdf"}
    )
