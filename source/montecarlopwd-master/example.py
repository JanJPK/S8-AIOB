#!/usr/bin/env python3

# Copyright 2016 Symantec Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0

# standard library
import argparse
import csv
import sys
import os

# internal imports
import backoff
import model
import ngram_chain
import pcfg

parser = argparse.ArgumentParser()
parser.add_argument('training_set', help='password training set')
parser.add_argument('password_set', help='password strength test set')
parser.add_argument('--min_ngram',
                    type=int,
                    default=2,
                    help='minimum n for n-grams')
parser.add_argument('--max_ngram',
                    type=int,
                    default=5,
                    help='maximum n for n-grams')
parser.add_argument('--backoff_threshold',
                    type=int,
                    default=10,
                    help='threshold for backoff')
parser.add_argument('--samplesize',
                    type=int,
                    default=10000,
                    help='sample size for Monte Carlo model')

required = parser.add_argument_group('required arguments')
args = parser.parse_args()

with open(args.training_set, 'rt') as f:
    training = [w.strip('\r\n') for w in f]

models = {
    '{}-gram'.format(i): ngram_chain.NGramModel(training, i)
    for i in range(args.min_ngram, args.max_ngram + 1)
}
models['Backoff'] = backoff.BackoffModel(training, 10)
models['PCFG'] = pcfg.PCFG(training)

samples = {
    name: list(model.sample(args.samplesize))
    for name, model in models.items()
}

estimators = {
    name: model.PosEstimator(sample)
    for name, sample in samples.items()
}
modelnames = sorted(models)

outfilename = f'./{os.path.splitext(args.password_set)[0]}_output.csv'
outfile = open(outfilename, 'w', encoding='utf-8', newline='')
writer = csv.writer(outfile)
writer.writerow(['password'] + modelnames)

with open(args.password_set, 'r', encoding='utf-8') as infile:
    for password in infile:
        password = password.strip('\r\n')
        estimations = [
            estimators[name].position(models[name].logprob(password))
            for name in modelnames
        ]
        writer.writerow([password] + estimations)

outfile.close()