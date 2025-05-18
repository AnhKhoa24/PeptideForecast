
import tensorflow as tf
class Attention(tf.keras.layers.Layer):
    def __init__(self, return_attention=False, **kwargs):
        super(Attention, self).__init__(**kwargs)
        self.return_attention = return_attention

    def build(self, input_shape):
        self.W = self.add_weight(name="att_weight", shape=(input_shape[-1], 1),
                                 initializer="normal")
        self.b = self.add_weight(name="att_bias", shape=(input_shape[1], 1),
                                 initializer="zeros")
        super().build(input_shape)

    def call(self, x):
        e = tf.keras.backend.tanh(tf.keras.backend.dot(x, self.W) + self.b)
        a = tf.keras.backend.softmax(e, axis=1)
        output = x * a
        if self.return_attention:
            return tf.keras.backend.sum(output, axis=1), a
        return tf.keras.backend.sum(output, axis=1)
