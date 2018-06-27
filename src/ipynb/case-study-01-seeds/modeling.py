import pandas as pd

def fit_and_score_lr_model_for_each_feature(lr_model, features, target):
    lm_scores = []
    for feat in features.columns:
        features_subset = features[[feat]]
        lr_model.fit(features_subset, target)
        lm_scores.append({
            'feature' : feat,
            'score' : lr_model.score(features_subset, target)
        })
    lm_scores_df = pd.DataFrame(lm_scores)
    lm_scores_df.set_index('feature', inplace=True)
    lm_scores_df = lm_scores_df.sort_values('score', ascending=False)
    return lm_scores_df
    