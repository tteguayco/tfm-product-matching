import pycrfsuite

import BIOTagger as biot

bio_tagger = biot.BIOTagger()
bio_tagger.tag_titles()

train_features = bio_tagger.get_titles_words_sequence()
train_labels = bio_tagger.get_titles_words_labels()

trainer = pycrfsuite.Trainer(verbose=True)

for xseq, yseq in zip(train_features, train_labels):
    trainer.append(xseq, yseq)

trainer.set_params({
    'c1': 0.1,
    'c2': 0.01,
    'max_iterations': 200,
    'feature.possible_transitions': True
})

trainer.train('crf.model')

tagger = pycrfsuite.Tagger()
tagger.open('crf.model')

y_pred = tagger.tag(['Nokia', '3', 'Version', '2018', 'Dual-SIM', 'silver'])

print(y_pred)
