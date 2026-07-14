# Portfolio Risk Engine

A tool built in python to calculate portfolio risk metrics (specifically Value
at Risk and Conditional Value at Risk) using historical, parametric, and Monte
Carlo methods. This is a re-implementation of a previous personal project, but
this time it is built around OOP so as to allow for the composition of a given
portfolio to change without having to reinput all the weights, securities, and
portfolio values. 

## Status

This project is heavily WIP, having been started 3 hours ago. So far, only some
classes have been properly implemented (`Position` and `Portfolio`). There are some
architectural choices I am yet to make, but I aim to implement risk calculation
next, in `methods.py`.

## Scope

This is solely being built as a risk engine, not a portfolio tracker. I have no
plans to implement cost basis, P&L, or trade history. Any future extension will
most likely be limited to implementing additional risk-specific metrics.