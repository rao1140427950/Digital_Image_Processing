import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

INPUT_NODE = 784
OUTPUT_NODE = 10

LAYER1_NODE = 500
BATCH_SIZE = 100
LEARNING_RATE_BASE = 0.8
LEARNING_RATE_DECAY = 0.99

REGULARIZATION_RATE = 0.0001
TRAINING_STEPS = 30000
MOVING_AVERAGE_DECAY = 0.99

MODE_SAVE_PATH = './checkpoint'

class network(object):

    __accuracy = None
    __x = None
    __y_ = None

    @classmethod
    def inference(cls, input_tensor, avg_class, weights1, biases1, weights2, biases2):
        if (avg_class == None):
            layer1 = tf.nn.relu(tf.matmul(input_tensor, weights1) + biases1)
            return tf.matmul(layer1, weights2) + biases2
        else:
            layer1 = tf.nn.relu(tf.matmul(input_tensor, avg_class.average(weights1)) + avg_class.average(biases1))
            return tf.matmul(layer1, avg_class.average(weights2)) + avg_class.average(biases2)

    
    @classmethod
    def initGraph(cls):
        #cls.__mnist = input_data.read_data_sets(DATA_PATH, one_hot = True)

        cls.__x = tf.placeholder(tf.float32, [None, INPUT_NODE], name = 'x_input')
        cls.__y_ = tf.placeholder(tf.float32, [None, OUTPUT_NODE], name = 'y_input')

        weights1 = tf.Variable(tf.truncated_normal([INPUT_NODE, LAYER1_NODE], stddev=0.1))
        biases1 = tf.Variable(tf.constant(0.1, shape=[LAYER1_NODE]))

        weights2 = tf.Variable(tf.truncated_normal([LAYER1_NODE, OUTPUT_NODE], stddev=0.1))
        biases2 = tf.Variable(tf.constant(0.1, shape=[OUTPUT_NODE]))

        y = cls.inference(cls.__x, None, weights1, biases1, weights2, biases2)
#        global_step = tf.Variable(0, trainable=False)
#
#        variable_averages = tf.train.ExponentialMovingAverage(MOVING_AVERAGE_DECAY, global_step)
#        variable_averages_op = variable_averages.apply(tf.trainable_variables())
#
#        average_y = cls.inference(cls.__x, variable_averages, weights1, biases1, weights2, biases2)

#        cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=tf.argmax(y_, 1), logits=y)
#        cross_entropy_mean = tf.reduce_mean(cross_entropy)
#
#        regularizer = tf.contrib.layers.l2_regularizer(REGULARIZATION_RATE)
#        regularization = regularizer(weights1) + regularizer(weights2)
#        loss = cross_entropy_mean + regularization
#
#        learning_rate = tf.train.exponential_decay(LEARNING_RATE_BASE, global_step, mnist.train.num_examples/BATCH_SIZE, LEARNING_RATE_DECAY)
#        train_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss, global_step=global_step)
#
#        with tf.control_dependencies([train_step, variable_averages_op]):
#            train_op = tf.no_op(name='train')

        correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(cls.__y_, 1))
        cls.__accuracy = tf.reduce_sum(tf.cast(correct_prediction, tf.float32))

    @classmethod
    def getTestAccuracy(cls, test_images, test_labels, num_examples):

        with tf.Session() as sess:
            saver = tf.train.Saver()
            save_model = tf.train.latest_checkpoint(MODE_SAVE_PATH)
            saver.restore(sess, save_model)
            acc = sess.run(cls.__accuracy, feed_dict = {cls.__x: test_images, cls.__y_: test_labels})
            
            return acc/num_examples



