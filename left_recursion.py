def removeLeftRecursion(rulesDiction):
	# for rule: A->Aa|b
	# result: A->bA',A'->aA'|#

	# 'store' has new rules to be added
	store = {}
	# traverse over rules
	for lhs in rulesDiction:
		# alphaRules stores subrules with left-recursion
		# betaRules stores subrules without left-recursion
		alphaRules = []
		betaRules = []
		# get rhs for current lhs
		allrhs = rulesDiction[lhs]
		for subrhs in allrhs:
			if subrhs[0] == lhs:
				alphaRules.append(subrhs[1:])
			else:
				betaRules.append(subrhs)
		# alpha and beta containing subrules are separated
		# now form two new rules
		if len(alphaRules) != 0:
			# to generate new unique symbol
			# add ' till unique not generated
			lhs_ = lhs + "'"
			while (lhs_ in rulesDiction.keys()) \
					or (lhs_ in store.keys()):
				lhs_ += "'"
			# make beta rule
			for b in range(0, len(betaRules)):
				betaRules[b].append(lhs_)
			rulesDiction[lhs] = betaRules
			# make alpha rule
			for a in range(0, len(alphaRules)):
				alphaRules[a].append(lhs_)
			alphaRules.append(['#'])
			# store in temp dict, append to
			# - rulesDiction at end of traversal
			store[lhs_] = alphaRules
	# add newly generated rules generated
	# - after removing left recursion
	for left in store:
		rulesDiction[left] = store[left]
	return rulesDiction

diction = {}

rules=["E -> E + T | T",
	 "T -> T * F | F",
	 "F -> ( E ) | id"
]

nonterm_userdef=['E','E\'','F','T','T\'']
term_userdef=['id','+','*','(',')']

for rule in rules:
    k = rule.split("->")
    # remove un-necessary spaces
    k[0] = k[0].strip()
    k[1] = k[1].strip()
    rhs = k[1]
    multirhs = rhs.split('|')
    # remove un-necessary spaces
    for i in range(len(multirhs)):
        multirhs[i] = multirhs[i].strip()
        multirhs[i] = multirhs[i].split()
    diction[k[0]] = multirhs
    
    print(f"\nRules: \n")
    for y in diction:
        print(f"{y}->{diction[y]}")
    print(f"\nAfter elimination of left recursion:\n")
    
    diction = removeLeftRecursion(diction)
    for y in diction:
        print(f"{y}->{diction[y]}")
    # print("\nAfter left factoring:\n")