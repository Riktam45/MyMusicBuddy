import json
from pathlib import Path

from ml.evaluation.metrics import calculate_metrics


TIME_TOLERANCE = 0.15


def load_notes(path: str):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def notes_match(predicted, truth):
    pitch_matches = (
        predicted["pitch"] == truth["pitch"]
    )

    start_difference = abs(
        predicted["start"] - truth["start"]
    )

    return (
        pitch_matches
        and start_difference <= TIME_TOLERANCE
    )


def evaluate(
    predicted_notes,
    ground_truth_notes,
):
    used_truth = set()

    true_positives = 0

    for predicted in predicted_notes:

        best_index = None
        best_difference = None

        for index, truth in enumerate(
            ground_truth_notes
        ):

            if index in used_truth:
                continue

            if not notes_match(
                predicted,
                truth,
            ):
                continue

            difference = abs(
                predicted["start"]
                - truth["start"]
            )

            if (
                best_difference is None
                or difference < best_difference
            ):
                best_difference = difference
                best_index = index

        if best_index is not None:
            used_truth.add(best_index)
            true_positives += 1

    false_positives = (
        len(predicted_notes)
        - true_positives
    )

    false_negatives = (
        len(ground_truth_notes)
        - true_positives
    )

    return calculate_metrics(
        true_positives=true_positives,
        false_positives=false_positives,
        false_negatives=false_negatives,
    )


if __name__ == "__main__":

    ground_truth_path = (
        Path(
            r"D:\mymusic-buddy\ml\evaluation"
            r"\ground_truth"
            r"\maps_alb_se3_ground_truth.json"
        )
    )

    prediction_path = (
        Path(
            r"D:\mymusic-buddy\ml\evaluation"
            r"\ground_truth"
            r"\maps_alb_se3_predictions.json"
        )
    )

    ground_truth = load_notes(
        ground_truth_path
    )

    predictions = load_notes(
        prediction_path
    )

    results = evaluate(
        predictions,
        ground_truth,
    )

    print()
    print("================================")
    print("   MyMusic Buddy ML Evaluation")
    print("================================")
    print()

    print(
        f"Ground-truth notes : "
        f"{len(ground_truth)}"
    )

    print(
        f"Predicted notes    : "
        f"{len(predictions)}"
    )

    print(
        f"True positives     : "
        f"{results['true_positives']}"
    )

    print(
        f"False positives    : "
        f"{results['false_positives']}"
    )

    print(
        f"False negatives    : "
        f"{results['false_negatives']}"
    )

    print()

    print(
        f"Precision          : "
        f"{results['precision']:.4f}"
    )

    print(
        f"Recall             : "
        f"{results['recall']:.4f}"
    )

    print(
        f"F1 Score           : "
        f"{results['f1']:.4f}"
    )

    print()