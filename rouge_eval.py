# backend/rouge_eval.py
import evaluate

rouge = evaluate.load("rouge")


def compute_rouge(system_summary, reference_summary):
    return rouge.compute(
        predictions=[system_summary],
        references=[reference_summary]
    )
