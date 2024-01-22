# Isoforms benchmark

This repo contains data on 18 isoforms which had previously been identified in literature as containing splice events in the middle of structure domains. We found that in AF2, OmegaFold, ESMFold, many of these result in erroneous structure predictions. We present this benchmark in the hopes that it can be used to identify non-biophysically-realistic errors in structure prediction methods.

## Models:

Structure models were generated in

 - AlphaFold2 [ColabFold notebook](https://colab.research.google.com/github/sokrypton/ColabFold/blob/main/AlphaFold2.ipynb)

 - OmegaFold [OmegaFold notebook](https://colab.research.google.com/github/sokrypton/ColabFold/blob/main/beta/omegafold.ipynb)

 - ESMFold [ESMFold web server](https://esmatlas.com/resources?action=fold)

using default settings for all.

## Scripts:

We provide information to calculate the Surface Aggregation Propensity score for structure models.
