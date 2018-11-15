import sys

inp_file = []
for line in sys.stdin:
	inp_file.append(line)

star_stack = []
out = []
stack_top = None
for i,line in enumerate(inp_file):
	# Ignore empty lines
	if line[0] == '\n':
		continue

	# Handle numbered items :
	# Maintain a stack for indices with elements (len(stars), index) where 
	# len(stars) indicates subitem depth and index holds complete index to be output
	elif line[0] == '*':
		stars = line.split(' ')[0]
		if len(star_stack) > 0:  
			stack_top = star_stack[-1]
			if stack_top[0] == len(stars):
				st_top_lst = stack_top[1].split('.')
				st_top_lst[-1] = str(int(st_top_lst[-1]) + 1)
				index = '.'.join(st_top_lst)
				star_stack.pop()
				star_stack.append((len(stars),index))
			elif stack_top[0] < len(stars):
				index = stack_top[1] + '.1'
				star_stack.append((len(stars),index))
			else:
				while stack_top[0] > len(stars) and len(star_stack) > 0:
					stack_top = star_stack.pop()
				st_top_lst = stack_top[1].split('.')
				st_top_lst[-1] = str(int(st_top_lst[-1]) + 1)
				index = '.'.join(st_top_lst)
				star_stack.append((len(stars),index))
		else:
			index = '1'
			star_stack.append((len(stars), index))
		out_line = index + line[len(stars):]
		out.append(out_line)

	# Handle subitems :
	# Decide case by case basis if the line can be expanded 
	elif line[0] == '.':
		next_line = inp_file[i+1]
		dots = line.split(' ')[0]
		ln_dts = len(dots)
		space = ''
		while ln_dts > 0:
			space += ' '
			ln_dts -= 1
		k = i
		while (next_line[0] == '\n' or (next_line[0] != '*' and next_line[0] != '.')) and k < len(inp_file)-1:
			next_line = inp_file[k+1]
			k += 1

		next_line_init = next_line.split(' ')[0]
		if next_line_init[0] == '*' or (next_line_init[0] == '.' and len(next_line_init) == len(dots)):
			prefix = '-' 
		elif (next_line_init[0] == '.' and len(next_line_init) > len(dots)):
			prefix = '+'
		else:
			prefix = '-'
		prev_line_space = space
		out_line = space + prefix + line[len(dots):]
		out.append(out_line)

	# Handle multiple lines of same subitem
	else:
		out_line = prev_line_space + line.lstrip()
		out.append(out_line)

for ln in out:
	sys.stdout.write(ln)
