import pycrfsuite

training_set = [
    (['Apple', 'iPhone', '4', '64', 'GB', '-', 'Gold'], ['BRAND', 'NAME', 'EDITION', 'MEM', 'MEM-UNIT', 'I', 'COLOR'])
]

trainer = pycrfsuite.Trainer(verbose=True)

for entity_pair in training_set:
    trainer.append(entity_pair[0], entity_pair[1])

trainer.set_params({
    'c1': 0.1,
    'c2': 0.01,
    'max_iterations': 200,
    'feature.possible_transitions': True
})

trainer.train('crf.model')

tagger = pycrfsuite.Tagger()
tagger.open('crf.model')

y_pred = tagger.tag(['iPhone', '5'])

print(y_pred)
