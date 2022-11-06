def LeftFactoring(rulesDiction):
	# for rule: A->aDF|aCV|k
	# result: A->aA'|k, A'->DF|CV

	# newDict stores newly generated
	# - rules after left factoring
	newDict = {}
	# iterate over all rules of dictionary
	for lhs in rulesDiction:
		# get rhs for given lhs
		allrhs = rulesDiction[lhs]
		# temp dictionary helps detect left factoring
		temp = dict()
		for subrhs in allrhs:
			if subrhs[0] not in list(temp.keys()):
				temp[subrhs[0]] = [subrhs]
			else:
				temp[subrhs[0]].append(subrhs)
		# if value list count for any key in temp is > 1,
		# - it has left factoring
		# new_rule stores new subrules for current LHS symbol
		new_rule = []
		# temp_dict stores new subrules for left factoring
		tempo_dict = {}
		for term_key in temp:
			# get value from temp for term_key
			allStartingWithTermKey = temp[term_key]
			if len(allStartingWithTermKey) > 1:
				# left factoring required
				# to generate new unique symbol
				# - add ' till unique not generated
				lhs_ = lhs + "'"
				while (lhs_ in rulesDiction.keys()) \
						or (lhs_ in tempo_dict.keys()):
					lhs_ += "'"
				# append the left factored result
				new_rule.append([term_key, lhs_])
				# add expanded rules to tempo_dict
				ex_rules = []
				for g in temp[term_key]:
					ex_rules.append(g[1:])
				tempo_dict[lhs_] = ex_rules
			else:
				# no left factoring required
				new_rule.append(allStartingWithTermKey[0])
		# add original rule
		newDict[lhs] = new_rule
		# add newly generated rules after left factoring
		for key in tempo_dict:
			newDict[key] = tempo_dict[key]
	return newDict



rules=["S -> A k O",
	"A -> A d | a B | a C",
	"C -> c",
	"B -> b B C | r"]

nonterm_userdef=['A','B','C']
term_userdef=['k','O','d','a','c','b','r']

diction = {}

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
	
diction = LeftFactoring(diction)
print(f"\nAfter Left Factoring: \n")
for y in diction:
    print(f"{y}->{diction[y]}")