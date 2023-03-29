



singlemodels = {}

singlemodels['poetic_features'] = ["models/lindep/stanzaCounter.py",
                                    "models/lindep/lineCounter.py",
                                    "models/en/syllableCounter.py",
                                    "models/en/stressSimple.py",
                                    "models/en/rhyme.py"]

singlemodels['novelty_features'] = ['models/lindep/intraNoveltyRouge.py']
singlemodels['fluency_features'] = []
singlemodels['lexsem_features'] = []

collectionmodels = {}
collectionmodels['poetic_features']  = []
collectionmodels['novelty_features'] = ['models/lindep/noveltyRouge.py']
collectionmodels['fluency_features'] = []
collectionmodels['lexsem_features']  = []
