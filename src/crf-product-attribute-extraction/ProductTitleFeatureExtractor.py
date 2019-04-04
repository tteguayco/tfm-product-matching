import pycrfsuite

crf_tagger = pycrfsuite.Tagger()
crf_tagger.open("./out/crf.model")

labels = crf_tagger.tag("Funda Samsung Galaxy S8 Plus, Coodio Funda Cuero Galaxy S8 Plus, Funda Cartera Billetera Wallet"
                        " Case, Cierre Magnético, Ranuras para Tarjetas, Soporte Plegable Para Samsung Galaxy S8 Plus, Negro".split())
prob = crf_tagger.probability(labels)

print("-> {}".format(crf_tagger.info()))
print("-> {}".format(labels))
print("-> {}".format(prob))
