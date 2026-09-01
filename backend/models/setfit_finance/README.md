---
tags:
- setfit
- sentence-transformers
- text-classification
- generated_from_setfit_trainer
widget:
- text: Create a new insurance product for young professionals.
- text: What was the yield on earning assets for FY2025?
- text: Show the NIM breakdown by loan category for Q2 2026.
- text: Calculate the cash flow to debt ratio for the trailing 12 months.
- text: Show operating income for Premium Savings Account.
metrics:
- accuracy
pipeline_tag: text-classification
library_name: setfit
inference: true
base_model: BAAI/bge-small-en-v1.5
---

# SetFit with BAAI/bge-small-en-v1.5

This is a [SetFit](https://github.com/huggingface/setfit) model that can be used for Text Classification. This SetFit model uses [BAAI/bge-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5) as the Sentence Transformer embedding model. A [LogisticRegression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html) instance is used for classification.

The model has been trained using an efficient few-shot learning technique that involves:

1. Fine-tuning a [Sentence Transformer](https://www.sbert.net) with contrastive learning.
2. Training a classification head with features from the fine-tuned Sentence Transformer.

## Model Details

### Model Description
- **Model Type:** SetFit
- **Sentence Transformer body:** [BAAI/bge-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5)
- **Classification head:** a [LogisticRegression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html) instance
- **Maximum Sequence Length:** 512 tokens
- **Number of Classes:** 4 classes
<!-- - **Training Dataset:** [Unknown](https://huggingface.co/datasets/unknown) -->
<!-- - **Language:** Unknown -->
<!-- - **License:** Unknown -->

### Model Sources

- **Repository:** [SetFit on GitHub](https://github.com/huggingface/setfit)
- **Paper:** [Efficient Few-Shot Learning Without Prompts](https://arxiv.org/abs/2209.11055)
- **Blogpost:** [SetFit: Efficient Few-Shot Learning Without Prompts](https://huggingface.co/blog/setfit)

### Model Labels
| Label               | Examples                                                                                                                                                                                                                    |
|:--------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| liquidity_agent     | <ul><li>'Show me working capital by division for Q1 2025.'</li><li>"What's our cash burn rate this quarter?"</li><li>'What is the cash conversion cycle for Mutual Fund Series 1?'</li></ul>                                |
| product_agent       | <ul><li>'Set up a new product bundle including Insurance Plan Alpha.'</li><li>'What is the product code for Insurance Plan Alpha?'</li><li>'Create a limited-time pricing offer for the Student Savings Account.'</li></ul> |
| knowledge_agent     | <ul><li>'Hey there!'</li><li>'Can you explain what NSFR means in banking?'</li><li>'What is a reserve requirement, generally speaking?'</li></ul>                                                                           |
| profitability_agent | <ul><li>'Calculate the interest margin on the mortgage book for the last 2 months.'</li><li>'Confirm our EBITDA for last quarter.'</li><li>'What was the yield on earning assets for FY2025?'</li></ul>                     |

## Uses

### Direct Use for Inference

First install the SetFit library:

```bash
pip install setfit
```

Then you can load this model and run inference.

```python
from setfit import SetFitModel

# Download from the 🤗 Hub
model = SetFitModel.from_pretrained("setfit_model_id")
# Run inference
preds = model("What was the yield on earning assets for FY2025?")
```

<!--
### Downstream Use

*List how someone could finetune this model on their own dataset.*
-->

<!--
### Out-of-Scope Use

*List how the model may foreseeably be misused and address what users ought not to do with the model.*
-->

<!--
## Bias, Risks and Limitations

*What are the known or foreseeable issues stemming from this model? You could also flag here known failure cases or weaknesses of the model.*
-->

<!--
### Recommendations

*What are recommendations with respect to the foreseeable issues? For example, filtering explicit content.*
-->

## Training Details

### Training Set Metrics
| Training set | Min | Median | Max |
|:-------------|:----|:-------|:----|
| Word count   | 1   | 8.4    | 17  |

| Label               | Training Sample Count |
|:--------------------|:----------------------|
| profitability_agent | 80                    |
| liquidity_agent     | 80                    |
| product_agent       | 80                    |
| knowledge_agent     | 80                    |

### Training Hyperparameters
- batch_size: (16, 16)
- num_epochs: (3, 3)
- max_steps: -1
- sampling_strategy: oversampling
- body_learning_rate: (2e-05, 1e-05)
- head_learning_rate: 0.01
- loss: CosineSimilarityLoss
- distance_metric: cosine_distance
- margin: 0.25
- end_to_end: False
- use_amp: False
- warmup_proportion: 0.1
- l2_weight: 0.01
- seed: 42
- eval_max_steps: -1
- load_best_model_at_end: False

### Training Results
| Epoch  | Step  | Training Loss | Validation Loss |
|:------:|:-----:|:-------------:|:---------------:|
| 0.0002 | 1     | 0.1857        | -               |
| 0.0104 | 50    | 0.2271        | -               |
| 0.0208 | 100   | 0.2321        | -               |
| 0.0312 | 150   | 0.2251        | -               |
| 0.0417 | 200   | 0.217         | -               |
| 0.0521 | 250   | 0.2034        | -               |
| 0.0625 | 300   | 0.1863        | -               |
| 0.0729 | 350   | 0.1624        | -               |
| 0.0833 | 400   | 0.1316        | -               |
| 0.0938 | 450   | 0.0843        | -               |
| 0.1042 | 500   | 0.0878        | -               |
| 0.1146 | 550   | 0.0779        | -               |
| 0.125  | 600   | 0.0626        | -               |
| 0.1354 | 650   | 0.0538        | -               |
| 0.1458 | 700   | 0.039         | -               |
| 0.1562 | 750   | 0.025         | -               |
| 0.1667 | 800   | 0.0096        | -               |
| 0.1771 | 850   | 0.0061        | -               |
| 0.1875 | 900   | 0.0043        | -               |
| 0.1979 | 950   | 0.0036        | -               |
| 0.2083 | 1000  | 0.0031        | -               |
| 0.2188 | 1050  | 0.0029        | -               |
| 0.2292 | 1100  | 0.0024        | -               |
| 0.2396 | 1150  | 0.0022        | -               |
| 0.25   | 1200  | 0.002         | -               |
| 0.2604 | 1250  | 0.0018        | -               |
| 0.2708 | 1300  | 0.0016        | -               |
| 0.2812 | 1350  | 0.0015        | -               |
| 0.2917 | 1400  | 0.0014        | -               |
| 0.3021 | 1450  | 0.0014        | -               |
| 0.3125 | 1500  | 0.0013        | -               |
| 0.3229 | 1550  | 0.0012        | -               |
| 0.3333 | 1600  | 0.0012        | -               |
| 0.3438 | 1650  | 0.0011        | -               |
| 0.3542 | 1700  | 0.001         | -               |
| 0.3646 | 1750  | 0.001         | -               |
| 0.375  | 1800  | 0.001         | -               |
| 0.3854 | 1850  | 0.0009        | -               |
| 0.3958 | 1900  | 0.001         | -               |
| 0.4062 | 1950  | 0.0009        | -               |
| 0.4167 | 2000  | 0.0008        | -               |
| 0.4271 | 2050  | 0.0008        | -               |
| 0.4375 | 2100  | 0.0008        | -               |
| 0.4479 | 2150  | 0.0008        | -               |
| 0.4583 | 2200  | 0.0008        | -               |
| 0.4688 | 2250  | 0.0008        | -               |
| 0.4792 | 2300  | 0.0008        | -               |
| 0.4896 | 2350  | 0.0007        | -               |
| 0.5    | 2400  | 0.0007        | -               |
| 0.5104 | 2450  | 0.0006        | -               |
| 0.5208 | 2500  | 0.0007        | -               |
| 0.5312 | 2550  | 0.0006        | -               |
| 0.5417 | 2600  | 0.0006        | -               |
| 0.5521 | 2650  | 0.0006        | -               |
| 0.5625 | 2700  | 0.0006        | -               |
| 0.5729 | 2750  | 0.0006        | -               |
| 0.5833 | 2800  | 0.0006        | -               |
| 0.5938 | 2850  | 0.0006        | -               |
| 0.6042 | 2900  | 0.0006        | -               |
| 0.6146 | 2950  | 0.0006        | -               |
| 0.625  | 3000  | 0.0006        | -               |
| 0.6354 | 3050  | 0.0005        | -               |
| 0.6458 | 3100  | 0.0005        | -               |
| 0.6562 | 3150  | 0.0005        | -               |
| 0.6667 | 3200  | 0.0005        | -               |
| 0.6771 | 3250  | 0.0005        | -               |
| 0.6875 | 3300  | 0.0005        | -               |
| 0.6979 | 3350  | 0.0005        | -               |
| 0.7083 | 3400  | 0.0005        | -               |
| 0.7188 | 3450  | 0.0005        | -               |
| 0.7292 | 3500  | 0.0004        | -               |
| 0.7396 | 3550  | 0.0004        | -               |
| 0.75   | 3600  | 0.0004        | -               |
| 0.7604 | 3650  | 0.0005        | -               |
| 0.7708 | 3700  | 0.0004        | -               |
| 0.7812 | 3750  | 0.0004        | -               |
| 0.7917 | 3800  | 0.0004        | -               |
| 0.8021 | 3850  | 0.0004        | -               |
| 0.8125 | 3900  | 0.0005        | -               |
| 0.8229 | 3950  | 0.0004        | -               |
| 0.8333 | 4000  | 0.0004        | -               |
| 0.8438 | 4050  | 0.0004        | -               |
| 0.8542 | 4100  | 0.0004        | -               |
| 0.8646 | 4150  | 0.0004        | -               |
| 0.875  | 4200  | 0.0004        | -               |
| 0.8854 | 4250  | 0.0004        | -               |
| 0.8958 | 4300  | 0.0004        | -               |
| 0.9062 | 4350  | 0.0004        | -               |
| 0.9167 | 4400  | 0.0004        | -               |
| 0.9271 | 4450  | 0.0004        | -               |
| 0.9375 | 4500  | 0.0004        | -               |
| 0.9479 | 4550  | 0.0004        | -               |
| 0.9583 | 4600  | 0.0004        | -               |
| 0.9688 | 4650  | 0.0004        | -               |
| 0.9792 | 4700  | 0.0004        | -               |
| 0.9896 | 4750  | 0.0004        | -               |
| 1.0    | 4800  | 0.0004        | -               |
| 1.0104 | 4850  | 0.0003        | -               |
| 1.0208 | 4900  | 0.0004        | -               |
| 1.0312 | 4950  | 0.0004        | -               |
| 1.0417 | 5000  | 0.0004        | -               |
| 1.0521 | 5050  | 0.0004        | -               |
| 1.0625 | 5100  | 0.0003        | -               |
| 1.0729 | 5150  | 0.0003        | -               |
| 1.0833 | 5200  | 0.0003        | -               |
| 1.0938 | 5250  | 0.0003        | -               |
| 1.1042 | 5300  | 0.0003        | -               |
| 1.1146 | 5350  | 0.0003        | -               |
| 1.125  | 5400  | 0.0003        | -               |
| 1.1354 | 5450  | 0.0003        | -               |
| 1.1458 | 5500  | 0.0004        | -               |
| 1.1562 | 5550  | 0.0003        | -               |
| 1.1667 | 5600  | 0.0003        | -               |
| 1.1771 | 5650  | 0.0003        | -               |
| 1.1875 | 5700  | 0.0003        | -               |
| 1.1979 | 5750  | 0.0003        | -               |
| 1.2083 | 5800  | 0.0003        | -               |
| 1.2188 | 5850  | 0.0003        | -               |
| 1.2292 | 5900  | 0.0003        | -               |
| 1.2396 | 5950  | 0.0003        | -               |
| 1.25   | 6000  | 0.0003        | -               |
| 1.2604 | 6050  | 0.0003        | -               |
| 1.2708 | 6100  | 0.0003        | -               |
| 1.2812 | 6150  | 0.0003        | -               |
| 1.2917 | 6200  | 0.0003        | -               |
| 1.3021 | 6250  | 0.0003        | -               |
| 1.3125 | 6300  | 0.0003        | -               |
| 1.3229 | 6350  | 0.0003        | -               |
| 1.3333 | 6400  | 0.0003        | -               |
| 1.3438 | 6450  | 0.0003        | -               |
| 1.3542 | 6500  | 0.0003        | -               |
| 1.3646 | 6550  | 0.0003        | -               |
| 1.375  | 6600  | 0.0003        | -               |
| 1.3854 | 6650  | 0.0003        | -               |
| 1.3958 | 6700  | 0.0003        | -               |
| 1.4062 | 6750  | 0.0003        | -               |
| 1.4167 | 6800  | 0.0003        | -               |
| 1.4271 | 6850  | 0.0003        | -               |
| 1.4375 | 6900  | 0.0003        | -               |
| 1.4479 | 6950  | 0.0003        | -               |
| 1.4583 | 7000  | 0.0003        | -               |
| 1.4688 | 7050  | 0.0003        | -               |
| 1.4792 | 7100  | 0.0003        | -               |
| 1.4896 | 7150  | 0.0003        | -               |
| 1.5    | 7200  | 0.0003        | -               |
| 1.5104 | 7250  | 0.0003        | -               |
| 1.5208 | 7300  | 0.0003        | -               |
| 1.5312 | 7350  | 0.0003        | -               |
| 1.5417 | 7400  | 0.0003        | -               |
| 1.5521 | 7450  | 0.0003        | -               |
| 1.5625 | 7500  | 0.0003        | -               |
| 1.5729 | 7550  | 0.0003        | -               |
| 1.5833 | 7600  | 0.0003        | -               |
| 1.5938 | 7650  | 0.0003        | -               |
| 1.6042 | 7700  | 0.0003        | -               |
| 1.6146 | 7750  | 0.0003        | -               |
| 1.625  | 7800  | 0.0003        | -               |
| 1.6354 | 7850  | 0.0003        | -               |
| 1.6458 | 7900  | 0.0003        | -               |
| 1.6562 | 7950  | 0.0003        | -               |
| 1.6667 | 8000  | 0.0003        | -               |
| 1.6771 | 8050  | 0.0003        | -               |
| 1.6875 | 8100  | 0.0003        | -               |
| 1.6979 | 8150  | 0.0003        | -               |
| 1.7083 | 8200  | 0.0003        | -               |
| 1.7188 | 8250  | 0.0003        | -               |
| 1.7292 | 8300  | 0.0003        | -               |
| 1.7396 | 8350  | 0.0003        | -               |
| 1.75   | 8400  | 0.0002        | -               |
| 1.7604 | 8450  | 0.0002        | -               |
| 1.7708 | 8500  | 0.0003        | -               |
| 1.7812 | 8550  | 0.0003        | -               |
| 1.7917 | 8600  | 0.0003        | -               |
| 1.8021 | 8650  | 0.0003        | -               |
| 1.8125 | 8700  | 0.0003        | -               |
| 1.8229 | 8750  | 0.0003        | -               |
| 1.8333 | 8800  | 0.0002        | -               |
| 1.8438 | 8850  | 0.0003        | -               |
| 1.8542 | 8900  | 0.0003        | -               |
| 1.8646 | 8950  | 0.0002        | -               |
| 1.875  | 9000  | 0.0002        | -               |
| 1.8854 | 9050  | 0.0002        | -               |
| 1.8958 | 9100  | 0.0002        | -               |
| 1.9062 | 9150  | 0.0003        | -               |
| 1.9167 | 9200  | 0.0003        | -               |
| 1.9271 | 9250  | 0.0002        | -               |
| 1.9375 | 9300  | 0.0002        | -               |
| 1.9479 | 9350  | 0.0002        | -               |
| 1.9583 | 9400  | 0.0002        | -               |
| 1.9688 | 9450  | 0.0002        | -               |
| 1.9792 | 9500  | 0.0003        | -               |
| 1.9896 | 9550  | 0.0002        | -               |
| 2.0    | 9600  | 0.0002        | -               |
| 2.0104 | 9650  | 0.0002        | -               |
| 2.0208 | 9700  | 0.0002        | -               |
| 2.0312 | 9750  | 0.0002        | -               |
| 2.0417 | 9800  | 0.0002        | -               |
| 2.0521 | 9850  | 0.0002        | -               |
| 2.0625 | 9900  | 0.0002        | -               |
| 2.0729 | 9950  | 0.0002        | -               |
| 2.0833 | 10000 | 0.0002        | -               |
| 2.0938 | 10050 | 0.0002        | -               |
| 2.1042 | 10100 | 0.0002        | -               |
| 2.1146 | 10150 | 0.0002        | -               |
| 2.125  | 10200 | 0.0002        | -               |
| 2.1354 | 10250 | 0.0002        | -               |
| 2.1458 | 10300 | 0.0002        | -               |
| 2.1562 | 10350 | 0.0002        | -               |
| 2.1667 | 10400 | 0.0002        | -               |
| 2.1771 | 10450 | 0.0002        | -               |
| 2.1875 | 10500 | 0.0002        | -               |
| 2.1979 | 10550 | 0.0002        | -               |
| 2.2083 | 10600 | 0.0002        | -               |
| 2.2188 | 10650 | 0.0002        | -               |
| 2.2292 | 10700 | 0.0002        | -               |
| 2.2396 | 10750 | 0.0002        | -               |
| 2.25   | 10800 | 0.0002        | -               |
| 2.2604 | 10850 | 0.0002        | -               |
| 2.2708 | 10900 | 0.0002        | -               |
| 2.2812 | 10950 | 0.0002        | -               |
| 2.2917 | 11000 | 0.0002        | -               |
| 2.3021 | 11050 | 0.0002        | -               |
| 2.3125 | 11100 | 0.0002        | -               |
| 2.3229 | 11150 | 0.0002        | -               |
| 2.3333 | 11200 | 0.0002        | -               |
| 2.3438 | 11250 | 0.0002        | -               |
| 2.3542 | 11300 | 0.0002        | -               |
| 2.3646 | 11350 | 0.0002        | -               |
| 2.375  | 11400 | 0.0002        | -               |
| 2.3854 | 11450 | 0.0002        | -               |
| 2.3958 | 11500 | 0.0002        | -               |
| 2.4062 | 11550 | 0.0002        | -               |
| 2.4167 | 11600 | 0.0002        | -               |
| 2.4271 | 11650 | 0.0002        | -               |
| 2.4375 | 11700 | 0.0002        | -               |
| 2.4479 | 11750 | 0.0002        | -               |
| 2.4583 | 11800 | 0.0002        | -               |
| 2.4688 | 11850 | 0.0002        | -               |
| 2.4792 | 11900 | 0.0002        | -               |
| 2.4896 | 11950 | 0.0002        | -               |
| 2.5    | 12000 | 0.0002        | -               |
| 2.5104 | 12050 | 0.0002        | -               |
| 2.5208 | 12100 | 0.0002        | -               |
| 2.5312 | 12150 | 0.0002        | -               |
| 2.5417 | 12200 | 0.0002        | -               |
| 2.5521 | 12250 | 0.0002        | -               |
| 2.5625 | 12300 | 0.0002        | -               |
| 2.5729 | 12350 | 0.0002        | -               |
| 2.5833 | 12400 | 0.0002        | -               |
| 2.5938 | 12450 | 0.0002        | -               |
| 2.6042 | 12500 | 0.0002        | -               |
| 2.6146 | 12550 | 0.0002        | -               |
| 2.625  | 12600 | 0.0002        | -               |
| 2.6354 | 12650 | 0.0002        | -               |
| 2.6458 | 12700 | 0.0002        | -               |
| 2.6562 | 12750 | 0.0002        | -               |
| 2.6667 | 12800 | 0.0002        | -               |
| 2.6771 | 12850 | 0.0002        | -               |
| 2.6875 | 12900 | 0.0002        | -               |
| 2.6979 | 12950 | 0.0002        | -               |
| 2.7083 | 13000 | 0.0002        | -               |
| 2.7188 | 13050 | 0.0002        | -               |
| 2.7292 | 13100 | 0.0002        | -               |
| 2.7396 | 13150 | 0.0002        | -               |
| 2.75   | 13200 | 0.0002        | -               |
| 2.7604 | 13250 | 0.0002        | -               |
| 2.7708 | 13300 | 0.0002        | -               |
| 2.7812 | 13350 | 0.0002        | -               |
| 2.7917 | 13400 | 0.0002        | -               |
| 2.8021 | 13450 | 0.0002        | -               |
| 2.8125 | 13500 | 0.0002        | -               |
| 2.8229 | 13550 | 0.0002        | -               |
| 2.8333 | 13600 | 0.0002        | -               |
| 2.8438 | 13650 | 0.0002        | -               |
| 2.8542 | 13700 | 0.0002        | -               |
| 2.8646 | 13750 | 0.0002        | -               |
| 2.875  | 13800 | 0.0002        | -               |
| 2.8854 | 13850 | 0.0002        | -               |
| 2.8958 | 13900 | 0.0002        | -               |
| 2.9062 | 13950 | 0.0002        | -               |
| 2.9167 | 14000 | 0.0002        | -               |
| 2.9271 | 14050 | 0.0002        | -               |
| 2.9375 | 14100 | 0.0002        | -               |
| 2.9479 | 14150 | 0.0002        | -               |
| 2.9583 | 14200 | 0.0002        | -               |
| 2.9688 | 14250 | 0.0002        | -               |
| 2.9792 | 14300 | 0.0002        | -               |
| 2.9896 | 14350 | 0.0002        | -               |
| 3.0    | 14400 | 0.0002        | -               |

### Framework Versions
- Python: 3.11.9
- SetFit: 1.1.3
- Sentence Transformers: 3.3.1
- Transformers: 4.44.2
- PyTorch: 2.13.0+cpu
- Datasets: 5.0.1
- Tokenizers: 0.19.1

## Citation

### BibTeX
```bibtex
@article{https://doi.org/10.48550/arxiv.2209.11055,
    doi = {10.48550/ARXIV.2209.11055},
    url = {https://arxiv.org/abs/2209.11055},
    author = {Tunstall, Lewis and Reimers, Nils and Jo, Unso Eun Seo and Bates, Luke and Korat, Daniel and Wasserblat, Moshe and Pereg, Oren},
    keywords = {Computation and Language (cs.CL), FOS: Computer and information sciences, FOS: Computer and information sciences},
    title = {Efficient Few-Shot Learning Without Prompts},
    publisher = {arXiv},
    year = {2022},
    copyright = {Creative Commons Attribution 4.0 International}
}
```

<!--
## Glossary

*Clearly define terms in order to be accessible across audiences.*
-->

<!--
## Model Card Authors

*Lists the people who create the model card, providing recognition and accountability for the detailed work that goes into its construction.*
-->

<!--
## Model Card Contact

*Provides a way for people who have updates to the Model Card, suggestions, or questions, to contact the Model Card authors.*
-->