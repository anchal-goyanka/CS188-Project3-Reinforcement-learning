# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
	for i in range(0,iterations):
		b = self.values.copy()
		#print ('b',b)
		#print ('all',mdp.getStates())
		for s in mdp.getStates():
		    if s == 'TERMINAL_STATE':
				self.values[s]= 0
		    else:
			#print ('s',s)
			qlist = []
			for a in mdp.getPossibleActions(s):
				if a =='exit':
					qlist.append(mdp.getReward(s,a,(mdp.getTransitionStatesAndProbs(s,a))))
				else:
					#print('a',a)
					spsum = 0
					for sp in mdp.getTransitionStatesAndProbs(s,a):
						#print('sp',sp)
						#print(mdp.getReward(s,a,sp[0]))
						spsum =spsum+ (sp[1]*(mdp.getReward(s,a,sp[0])+self.discount*b[sp[0]]))
						#print ('spsum',spsum)
						#print('i',i)
					qlist.append(spsum)
			#print qlist
			self.values[s] = max(qlist)
			while len(qlist) > 0 : qlist.pop()	
				


        # Write value iteration code here
        "*** YOUR CODE HERE ***"


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
	qvalue = 0
	#print('qv',qvalue)
	
	for s in self.mdp.getTransitionStatesAndProbs(state,action):
		qvalue= qvalue+ (s[1]*(self.mdp.getReward(state,action,s[0])+self.discount*self.values[s[0]]))
	return qvalue
        util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
	ll = util.Counter()
	if (state == 'TERMINAL_STATE'):
		return None
	else:
		#print ('ac',self.mdp.getPossibleActions(state))
		for ac in self.mdp.getPossibleActions(state):
			ll[ac] = self.computeQValueFromValues(state, ac)
		return ll.argMax()


    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
