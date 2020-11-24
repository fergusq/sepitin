# SEPITIN

Iikka Hauhio & Petrus Peltola 2020

## Introduction

Our project aims to generate creative, coherent and compelling short stories. We got the idea from theNational Novel Generation Month, a popular spin-off to theNational Novel Writing Monthwhere the objective is to write a 50,000 words long piece of fiction in the month of November. When taking a closer look at the NaNoGenMo submissions, two things become apparent: they often lack narrative coherence and the content rarely captivates  the  reader. Both of these problems get worse when the length of the content grows, which is easy to notice when comparing shorter generated texts with the NaNoGenMo entries.

To tackle these issues we planned a twofold approach where we would first generate a plot and then translate the plot into natural language separately. We hope that by using this approach we can focus on the aforementioned issues separately: a good plot keeps the story coherent and better surface realization makes the content more engaging. Thus, our system consists of two parts: the plot generation and the realization of the story as natural language.
These two steps are somewhat separate, so we will describe them individually.

## Plot generation

## Natural language generation

After generating the story actions, we first translate them to an initial natural language representation using a template-based system. There is a human-written template for each story action into details like character names are inserted. This will result in a natural languge skeleton of the story.

Then, we use Transformer-based neural network to generate a longer text piece for each story action. The template-based text is used as a prompt for the neural network. We are currently training two transformer models, one based on publicly available news articles and one based on fanfiction short stories. We will test both models and select one that generates more compelling results.

The final product will then be either a series of short stories, a series of news articles, or a mixture of both. The generated articles will be independent, but our hope is that they will tell the story we want together.
