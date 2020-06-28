# Tensor Flow Video: https://www.youtube.com/watch?v=lKoPIQdRBME
# Text classification with an RNN: https://www.tensorflow.org/tutorials/text/text_classification_rnn
import tensorflow_datasets as tfds
import tensorflow as tf
import matplotlib.pyplot as plt

def plot_graphs(history, metric):
  plt.plot(history.history[metric])
  plt.plot(history.history['val_'+metric], '')
  plt.xlabel("Epochs")
  plt.ylabel(metric)
  plt.legend([metric, 'val_'+metric])
  plt.show()

dataset, info = tfds.load('imdb_reviews/subwords8k', with_info=True,
                          as_supervised=True)
train_dataset, test_dataset = dataset['train'], dataset['test']

encoder = info.features['text'].encoder

# ## start
# print('Vocabulary size: {}'.format(encoder.vocab_size))

# sample_string = 'Hello TensorFlow.'

# encoded_string = encoder.encode(sample_string)
# print('Encoded string is {}'.format(encoded_string))

# original_string = encoder.decode(encoded_string)
# print('The original string: "{}"'.format(original_string))

# assert original_string == sample_string

# for index in encoded_string:
#   print('{} ----> {}'.format(index, encoder.decode([index])))
# ### end

BUFFER_SIZE = 10000
BATCH_SIZE = 64


padded_shapes = ([None],())

train_dataset = train_dataset.shuffle(BUFFER_SIZE).padded_batch(BATCH_SIZE,padded_shapes=padded_shapes)
test_dataset = test_dataset.padded_batch(BATCH_SIZE,padded_shapes=padded_shapes)

# ###
# train_dataset = train_dataset.shuffle(BUFFER_SIZE)
# train_dataset = train_dataset.padded_batch(BATCH_SIZE)

# test_dataset = test_dataset.padded_batch(BATCH_SIZE)
# ###


#### get rid of this section when running second time<
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(encoder.vocab_size, 64),
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(loss=tf.keras.losses.BinaryCrossentropy(from_logits=True), # loss='binary_crossentropy'
              optimizer=tf.keras.optimizers.Adam(1e-4),
              metrics=['accuracy'])

history = model.fit(train_dataset, epochs=10,
                    validation_data=test_dataset, 
                    validation_steps=30) # get rid of this
#### >

def pad_to_size(vec, size):
	zeros=[0]*(size-len(vec))
	vec.extend(zeros)
	return vec

def sample_predict(sentence,pad):
	encoded_sample_pred_text = encoder.encode(sentence)
	if pad:
		encoded_sample_pred_text = pad_to_size(encoded_sample_pred_text,64)
	encoded_sample_pred_text = tf.cast(encoded_sample_pred_text, tf.float32)
	predictions = model.predict(tf.expand_dims(encoded_sample_pred_text,0))
	return predictions

#### as well as all this <
sample_text = ('This move was awesome. The acting was incredible. Highly Recommend.')
predictions = sample_predict(sample_text,pad=True)*100 # percentage

print('probabability of positive review %.2f' % predictions)

sample_text = ('This movie was so so. The acting was mediocre. Kind of Recommend')
predictions = sample_predict(sample_text, pad=True)*100
print('probabability of positive review %.2f' % predictions)
#### >

# intial output:





# Adding Complications
model = tf.keras.Sequential([tf.keras.layers.Embedding(encoder.vocab_size,64),
							tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64, return_sequences=True)),
							tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(32)),
							tf.keras.layers.Dense(64, activation='relu'),
							tf.keras.layers.Dropout(0.5),
							tf.keras.layers.Dense(1,activation='sigmoid')])
model.compile(loss='binary_crossentropy',
			optimizer=tf.keras.optimizers.Adam(1e-4),
			metrics=['accuracy'])

history = model.fit(train_dataset, epochs=5,validation_dataset=test_dataset, validation_steps=30)

sample_text = ('This move was awesome. The acting was incredible. Highly Recommend.')
predictions = sample_predict(sample_text,pad=True)*100 # percentage

print('probabability of positive review %.2f' % predictions)

sample_text = ('This movie was so so. The acting was mediocre. Kind of Recommend')
predictions = sample_predict(sample_text, pad=True)*100
print('probabability of positive review %.2f' % predictions)
