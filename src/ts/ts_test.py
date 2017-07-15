import tensorflow as tf
from src.utils.database import dbMeta

df = dbMeta.get_krx_latest_data()
tf_shape = list(df.shape)
df.drop(['time'], axis=1, inplace=True, errors='ignore')
mat = df.as_matrix()
print(mat)
dataVar_tensor = tf.constant(mat, dtype=tf.float32, shape=tf_shape)
print(dataVar_tensor)
# depth_tensor = tf.constant(depth, 'float32',shape=[15780,1])

# Each time we run these ops, different results are generated
sess = tf.Session()
# print(sess.run(norm))