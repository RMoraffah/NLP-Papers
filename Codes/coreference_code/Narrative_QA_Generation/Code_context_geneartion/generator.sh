python acl20_repro.py model sto ilm | bash
CACHE_DIR=cache
DATASET=NarrativeQA
EXAMPLES_DIR=data/char_masks/${DATASET}
python generate_ilm.py \
    experiment_${DATASET} \
    ${CACHE_DIR} \
    ${EXAMPLES_DIR} \
    --seed 0 \
    --train_examples_tag train \
    --train_max_num_examples 9054 
    --eval_examples_tag valid \
    --eval_max_num_examples 954 \ 
