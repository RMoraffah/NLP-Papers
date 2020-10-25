import tensorflow as tf
from embeddings import load_sentence_embeddings
from preprocess_data import preprocess_batch
from six.moves import input
from lstm_model import lstm_model
import numpy as np
from pprint import pprint as pp
import random

import json
import numpy as np

class Paraphraser(object):
    '''Heart of the paraphraser model.  This class loads the checkpoint
    into the Tensorflow runtime environment and is responsible for inference.
    Greedy and sampling based approaches are supported
    '''

    def __init__(self, checkpoint):
        """Constructor.  Load vocabulary index, start token, end token, unk id,
        mask_id.  Restore checkpoint.

        Args:
            checkpoint: A path to the checkpoint
        """
        self.word_to_id, self.idx_to_word, self.embedding, self.start_id, self.end_id, self.unk_id, self.mask_id = load_sentence_embeddings()
        self.checkpoint = checkpoint
        gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.5)
        self.sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))
        self.model = lstm_model(self.sess, 'infer', 300, self.embedding, self.start_id, self.end_id, self.mask_id)
        saver = tf.train.Saver()
        saver.restore(self.sess, checkpoint)

    def sample_paraphrase(self, sentence, sampling_temp=1.0, how_many=1):
        """Paraphrase by sampling a distribution

        Args:
            sentence (str): A sentence input that will be paraphrased by 
                sampling from distribution.
            sampling_temp (int) : A number between 0 an 1

        Returns:
            str: a candidate paraphrase of the `sentence`
        """

        return self.infer(1, sentence, self.idx_to_word, sampling_temp, how_many)

    def greedy_paraphrase(self, sentence):
        """Paraphrase using greedy sampler
    
        Args:
            sentence : The source sentence to be paraphrased.

        Returns:
            str : a candidate paraphrase of the `sentence`
        """

        return self.infer(0, sentence, self.idx_to_word, 0., 1)


    def infer(self, decoder, source_sent, id_to_vocab, temp, how_many):
        """ Perform inferencing.  In other words, generate a paraphrase
        for the source sentence.

        Args:
            decoder : 0 for greedy, 1 for sampling
            source_sent : source sentence to generate a paraphrase for
            id_to_vocab : dict of vocabulary index to word
            end_id : the end token
            temp : the sampling temperature to use when `decoder` is 1

        Returns:
            str : for the generated paraphrase
        """

        seq_source_words, seq_source_ids = preprocess_batch([ source_sent ] * how_many)
        #print(seq_source_words)
        #print(seq_source_ids)
        seq_source_len = [ len(seq_source) for seq_source in seq_source_ids ]
        #print(seq_source_len)

        feed_dict = {
            self.model['seq_source_ids']: seq_source_ids,
            self.model['seq_source_lengths']: seq_source_len,
            self.model['decoder_technique']: decoder,
            self.model['sampling_temperature']: temp
        }

        feeds = [
            self.model['predictions']
            #model['final_sequence_lengths']
        ]

        predictions = self.sess.run(feeds, feed_dict)[0]
        #print(predictions)
        return self.translate(predictions, decoder, id_to_vocab, seq_source_words[0])

    def translate(self, predictions, decoder, id_to_vocab, seq_source_words):
        """ Translate the vocabulary ids in `predictions` to actual words
        that compose the paraphrase.

        Args:
            predictions : arrays of vocabulary ids
            decoder : 0 for greedy, 1 for sample, 2 for beam
            id_to_vocab : dict of vocabulary index to word

        Returns:
            str : the paraphrase
        """
        translated_predictions = []
        #np_end = np.where(translated_predictions == end_id)
        for sent_pred in predictions:
            translated = []
            for pred in sent_pred:
                word = 'UUNNKK'
                if pred == self.end_id:
                    break
                if pred == self.unk_id:
                    # Search for rare word
                    for seq_source_word in seq_source_words:
                        if seq_source_word not in self.word_to_id:
                            word = seq_source_word
                else:
                    word = id_to_vocab[pred]
                translated.append(word)
            translated_predictions.append(' '.join(translated))
        return translated_predictions
   
# The job of the data loader is basically to load and stage data from the 
# parsed unanswerable qa json files and prepare it for model input. For each
# qa entity in the dataset, there is a (context, question, answer-list) triplet
# and we may want to paraphrase parts of any of these three elements in different
# ways depending on the data source.
class UnanswerableQADataHandler(object):
    def read_data(self): pass
    def gen_context_paraphrase_span_ind(self, qa_key): pass
    def gen_question_paraphrase_span_ind(self, qa_key): pass
    def gen_answer_paraphrase_span_ind(self, qa_key, answer_ind): pass
    def run(self): pass
        
class CosmosQADataHandler(UnanswerableQADataHandler):
    def __init__(self, 
                 paraphraser,
                 parsed_unanswerableqa_path,
                 paraphrased_data_path,
                 sampling_temp=0.5):
        self.paraphraser = paraphraser
        self.load_path = parsed_unanswerableqa_path
        self.save_path = paraphrased_data_path
        self.quail_nei_str = "not enough information"
        self.init = True
        self.sampling_temp = sampling_temp
        
    def read_data(self):
        with open(self.load_path,  mode='r', encoding="utf8") as f:
            self.qa_data = json.load(f)
        self.init = False
            
    def gen_context_paraphrase_span_ind(self, context):
        #context = self.data_dict[qa_key]['context']
        return None
    
    def gen_question_paraphrase_span_ind(self, question):
        #question = self.data_dict[qa_key]['question']
        return (0,len(question))
    
    def gen_answer_paraphrase_span_ind(self, answer):
        #answer = self.data_dict[qa_key]['answer'+str(answer_ind)]
        if self.quail_nei_str in answer:
            return None
        else:
            return (0,len(answer))
        
    def paraphrase_subspans(self, source, para_span, paraphrases_per_sample=1):
        paraphrases = np.full(paraphrases_per_sample, source, dtype=object)
        
        # If para_span is not None, then we want to paraphrase the subspans for this data source...
        if para_span != None:
            # Get the portion of the source which we will paraphrase
            source_subspan = source[para_span[0]:para_span[1]]
            
            # Generate the source subspan paraphrases
            subspan_paraphrases = self.paraphraser.sample_paraphrase(source_subspan, 
                                                                     sampling_temp=self.sampling_temp,
                                                                     how_many=paraphrases_per_sample)
            #subspan_paraphrases = np.array(subspan_paraphrases, dtype=object)
            
            if (para_span[1]-para_span[0]) == len(source):
                return subspan_paraphrases
            
            for k in range(paraphrases_per_sample):
                paraphrases[k] = source[:para_span[0]] + subspan_paraphrases[k] + source[para_span[1]:]    
        
        # Otherwise if we don't want to paraphrase source subspans for this
        # data source, we will just keep the original source as is.
        else:
            #subspan_paraphrases = np.full((1,paraphrases_per_sample), source, dtype=object)
            pass
            
        return paraphrases
        
    def run(self, paraphrases_per_sample=1):
        if self.init == True: # Only read data file on first run
            self.read_data()
            print("Finished reading the qa data in initial phase.")
            
        # For each qa entity which contains a (context, question, answer-list)
        # triple, generate and replace subspans of the text with new paraphrased
        # versions, based on data source paraphrasing methods.
        paraphrased_qa_entries = []
        for k, qa_entry in enumerate(self.qa_data):
            if k == 1268:
                continue
            
            if k % 10 == 0:
                print("Processing qa entry {} out of {}".format(k, len(self.qa_data)))
            
            # Process the context through the model
            context = qa_entry['Context']
            para_span = self.gen_context_paraphrase_span_ind(context)
            context_subspan_paraphrases = self.paraphrase_subspans(context, 
                                                                   para_span,
                                                                   paraphrases_per_sample)
                
            # Process the question through the model
            question = qa_entry['Question']
            para_span = self.gen_question_paraphrase_span_ind(question)
            question_subspan_paraphrases = self.paraphrase_subspans(question,
                                                                    para_span,
                                                                    paraphrases_per_sample)

            
            # Process the answer choices through the model. Note that only the
            # three distractor answer choices should be paraphrased for
            # unanswerable questions
            answer_choice_A = qa_entry['Choices']['A']
            para_span = self.gen_answer_paraphrase_span_ind(answer_choice_A)
            answerA_subspan_paraphrases = self.paraphrase_subspans(answer_choice_A,
                                                                   para_span,
                                                                   paraphrases_per_sample)
            
            
            answer_choice_B = qa_entry['Choices']['B']
            para_span = self.gen_answer_paraphrase_span_ind(answer_choice_B)
            answerB_subspan_paraphrases = self.paraphrase_subspans(answer_choice_B,
                                                                   para_span,
                                                                   paraphrases_per_sample)
            
            
            answer_choice_C = qa_entry['Choices']['C']
            para_span = self.gen_answer_paraphrase_span_ind(answer_choice_C)
            answerC_subspan_paraphrases = self.paraphrase_subspans(answer_choice_C,
                                                                   para_span,
                                                                   paraphrases_per_sample)
            
            answer_choice_D = qa_entry['Choices']['D']
            para_span = self.gen_answer_paraphrase_span_ind(answer_choice_D)
            answerD_subspan_paraphrases = self.paraphrase_subspans(answer_choice_D,
                                                                   para_span,
                                                                   paraphrases_per_sample)
            
            for par_itr in range(paraphrases_per_sample):
                paraphrased_qa_entry = {}
                paraphrased_qa_entry['Context'] = context_subspan_paraphrases[par_itr]
                paraphrased_qa_entry['Question'] = question_subspan_paraphrases[par_itr]
                paraphrased_qa_entry['Reasoning type'] = "Unanswerable"
                paraphrased_qa_entry['Choices'] = {}
                paraphrased_qa_entry['Choices']['A'] = answerA_subspan_paraphrases[par_itr]
                paraphrased_qa_entry['Choices']['B'] = answerB_subspan_paraphrases[par_itr]
                paraphrased_qa_entry['Choices']['C'] = answerC_subspan_paraphrases[par_itr]
                paraphrased_qa_entry['Choices']['D'] = answerD_subspan_paraphrases[par_itr]
                paraphrased_qa_entry['Answer'] = qa_entry['Answer']
                paraphrased_qa_entries.append(paraphrased_qa_entry)
                
                #if k % 10 == 0:
                #    print("{}\n{}\n\n".format(qa_entry, paraphrased_qa_entry))
                
        with open(self.save_path, 'w') as json_file:
            json.dump(paraphrased_qa_entries, json_file)
            
def interactive_paraphrasing(paraphraser):
    while 1:
        source_sentence = input("Source: ")
        #p = paraphraser.greedy_paraphrase(source_sentence)
        #print(p)
        paraphrases = paraphraser.sample_paraphrase(source_sentence, sampling_temp=0.25, how_many=10)
        for i, paraphrase in enumerate(paraphrases):
            print("Paraph #{}: {}".format(i, paraphrase))

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--checkpoint', type=str, help='Checkpoint path')
    args = parser.parse_args()
    paraphraser = Paraphraser(args.checkpoint)

    # Takes input from the 
    #interactive_paraphrasing(paraphraser)
    
    parsed_unanswerableqa_path = "../../../datasets/cosmos_qa/parsed_unanswerable/cosmos_qa_valid_unanswerable.json"
    paraphrased_data_output_path_base = "../../../datasets/cosmos_qa/parsed_unanswerable/cosmos_qa_valid_unanswerable_paraphrased"
    for sample_temp in np.array([0.2, 0.35, 0.45, 0.6, 0.75]):
        cosmos_qa_handler = CosmosQADataHandler(paraphraser, 
                                                parsed_unanswerableqa_path, 
                                                paraphrased_data_output_path_base + "_" + str(sample_temp) + ".json",
                                                sampling_temp=0.2)
        cosmos_qa_handler.run(paraphrases_per_sample=1)
    
if __name__ == '__main__':
    main()

