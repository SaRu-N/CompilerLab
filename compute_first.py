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

# pass rule in first function
def first(rule):
	# recursion base condition
	# (for terminal or epsilon)
	if len(rule) != 0 and (rule is not None):
		if rule[0] in term_userdef:
			return rule[0]
		elif rule[0] == '#':
			return '#'

	# condition for Non-Terminals
	if len(rule) != 0:
		if rule[0] in list(diction.keys()):
			# fres temporary list of result
			fres = []
			rhs_rules = diction[rule[0]]
			# call first on each rule of RHS
			# fetched (& take union)
			for itr in rhs_rules:
				indivRes = first(itr)
				if type(indivRes) is list:
					for i in indivRes:
						fres.append(i)
				else:
					fres.append(indivRes)

			# if no epsilon in result
			# - received return fres
			if '#' not in fres:
				return fres
			else:
				# apply epsilon
				# rule => f(ABC)=f(A)-{e} U f(BC)
				newList = []
				fres.remove('#')
				if len(rule) > 1:
					ansNew = first(rule[1:])
					if ansNew != None:
						if type(ansNew) is list:
							newList = fres + ansNew
						else:
							newList = fres + [ansNew]
					else:
						newList = fres
					return newList
				# if result is not already returned
				# - control reaches here
				# lastly if eplison still persists
				# - keep it in result of first
				fres.append('#')
				return fres
                


rules=["S -> A k O",
	"A -> A d | a B | a C",
	"C -> c",
	"B -> b B C | r"]

nonterm_userdef=['A','B','C']
term_userdef=['k','O','d','a','c','b','r']


# diction - store rules inputed
# firsts - store computed firsts
diction = {}
firsts = {}
follows = {}

# computes all FIRSTs for all non terminals
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
print("\nAfter left factoring:\n")

diction = LeftFactoring(diction)
for y in diction:
	print(f"{y}->{diction[y]}")

# calculate first for each rule
# - (call first() on all RHS)
for y in list(diction.keys()):
	t = set()
	for sub in diction.get(y):
		res = first(sub)
		if res != None:
			if type(res) is list:
				for u in res:
					t.add(u)
			else:
				t.add(res)

	# save result in 'firsts' list
	firsts[y] = t

print("\nCalculated firsts: ")
key_list = list(firsts.keys())
index = 0
for gg in firsts:
	print(f"first({key_list[index]}) "
		f"=> {firsts.get(gg)}")
	index += 1
# assuming first rule has start_symbol
# start symbol can be modified in below line of code
start_symbol = list(diction.keys())[0]
# computes all FOLLOWs for all occurrences