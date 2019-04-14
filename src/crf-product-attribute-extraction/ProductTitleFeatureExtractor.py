import pycrfsuite
from joblib import load

CRF_MODEL_PATHFILE = "./out/crf.joblib"

crf = load(CRF_MODEL_PATHFILE)

labels = crf.predict(["Funda Samsung Galaxy S8 Plus, Coodio Funda Cuero Galaxy S8 Plus, Funda Cartera Billetera Wallet"
                        " Case, Cierre Magnético, Ranuras para Tarjetas, Soporte Plegable Para Samsung Galaxy S8 Plus, Negro".split()])


print(labels)