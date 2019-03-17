import pycrfsuite

PRODUCT_DATA_PATH = "../../RawData/DataFinal/SmartphonesProductDataFinal.csv"

training_set = [
    (['Apple', 'iPhone', '4', '64', 'GB', '-', 'Gold'], ['B-BRAND', 'I-BRAND', 'EDITION', 'MEM', 'MEM-UNIT', 'I', 'COLOR'])
]

trainer = pycrfsuite.Trainer(verbose=True)

for seq in training_set:
    trainer.append(seq[0], seq[1])

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
