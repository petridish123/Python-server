# Summary

This is the prototype of a research tool used at BYU in dr. Crandall's lab.

This tool, when completed, will be implemented into another project called "GridHunt"

GridHunt (GH) is a fast pace real-time stag hare problem representation where
individuals will work together to either hunt the larger prey and all benefit
or hunt the smaller prey and scare off the bigger prey.

This tool will be implemented into GH to also model the social aspect of the stag hare problem,
using "sentiments."

Sentiments are how a player feels about another player.
A sentiment comes from {-2,-1,0,1,2} which is represented as words from 
{very negative, negative, neutral, positive, very positive}.

The hope is that as a player collaborates with another player, they will increase their sentiment
modeling relationships in this problem simulation.

After we model relationships in the problem, we hope to see if there is a trend
between the relationships and the success of an individual.

The end research goal is to find a relationship between relationships and success/
Social and economic success. This, we believe, will model real life
so that we can find how people in poverty stay there and how they can 
get out of poverty in the United States.

# How the tool (is supposed to) works

The tool consists of a server script (GameServer) found in the server directory, a shared script (game) found in the shared directory
and a client script (qtwebsocket) found in the client directory.

These three work together to create the client server connection and run the tool.

When the server is opened, it waits until X amount of people are connected, where X is the set number in the script.
When X amount are connected the server then sends a start game message.

In the future, this will implement a state machine, but so far this is not a feature.