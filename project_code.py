from project_utils import *
import networkx as nx
import numpy as np
from multiprocessing import Pool

#Function 1 
def split_longitude(network,longitude,destinations_list):
	'''splits rests home list into west and east groupos with respective to a given longitude
	----------
	Parameters:
	network: network
			 graph object contains the network 
	longitude: float 
			   the reference longitude
	destinations_list: list
					   list of names (str) of the nodes that are needed to split into  west and east 

	----------
	Returns: 
	west: list
		  list of names (str) of nodes that are in the west of the given longitude
	east: list
		  list of names (str) of the nodes that are in the east of the given longitude

	'''
	#Create 2 list west and east to store the names 
	west=[]
	east=[]

	#Loop through destinations_list 
	for node in destinations_list:
		#Get the longitude of the node 
		destination_lng=network.nodes[node]['lng']
		if destination_lng > longitude: #if it is in the right of the given longitude, then it's East
			east.append(node)
		else: #If it is in the left of the given longitude, then it's West
			west.append(node)

	#Return 
	return west, east

#Function 2 
def split_latitude(network,latitude,destinations_list):
	'''splits rests home list in to north and south with respect to latitude arguments
		----------
	Parameters:
	network: network
			 graph object contains the network 
	latitude: float 
			   the reference latitude
	destinations_list: list
					   list of names (str) of the nodes that are needed to split into north and south 

	----------
	Returns: 
	north: list
		  list of names (str) of nodes that are in the north of the given latitude
	south: list
		  list of names (str) of the nodes that are in the south of the given latitude
	'''

	#Create 2 list noth and south to store the names
	north=[]
	south=[]
	
	#Loop through destinations_list 
	for node in destinations_list:
		#Get the latitude of the node 
		destination_lat=network.nodes[node]['lat']
		if destination_lat > latitude: #If it is above the given latitude, then North
			north.append(node)
		else: #If it is below the given latitude, then South
			south.append(node)
	
	#Return 
	return north, south

#Function 3
def swap(A,index1,index2):
	'''
	swaps 2 elements in 2 given indices of a list 
	----------
	Parameters: 
	A: list,array 
	   list/array that contains elements need to be swapped 
	index1: int 
			index of the first element that needs to be swapped 
	index2: int
			index of the second elements that needs to be swapped 
	
	----------
	Note:
	The order of index1 and index2 does not matter. swap(A,1,2) and swap(A,2,1) gives same output 
	The list/array is modified in place 
	'''
	#make a copy of the elements in position index1
	copy_element=A[index1]

	#Swap 
	A[index1]=A[index2]
	A[index2]=copy_element

#Function 4 
def redirect(pairs):
	'''
	returns the new ordered list of pairs of nodes of the path (A-B),(B-C),...,(X-Y),(Y-Z)
	----------
	Parameters: 
	pairs: list
		   list of unordered pairs (tuples) of the nodes (A-D)(B-C)...
	
	----------
	Returns:
	path: list
		  an ordered list of the new path [A'-B'-C'...X'-Y'-Z']

	----------
	Note: 

	'''
	#Initialised list 
	path=[]
	path.append(pairs[0][0])
	path.append(pairs[0][1])
	pairs.remove(pairs[0])

	#Loop through the pairs
	check_inverse=False #the path is not invert initially 
	i=0
	while not(len(pairs) == 0):
		pair=pairs[i]
		#Not inverted
		if not(check_inverse):
			if pair[0] == path[-1]: #check for position 0, if matches, add, loop again 
				path.append(pair[1])
				pairs.remove(pair)
				i=0
				continue
			else: 
				i+=1
		#path is inverted
		elif check_inverse:
			if pair[1] == path[-1]: #check for position 1, if matches, add, loop again
				path.append(pair[0])
				pairs.remove(pair)
				i=0
				continue
			else: 
				i+=1

		#Condition
		if i==len(pairs):
			i=0
			check_inverse=not(check_inverse)
	
	return path

#Function 5 
def pairs_generator(path):
	'''
	Returns an ordered list of pairs generated from a list
	----------
	Parameters: 
	path: list
		  list of elements (nodes)

	----------
	Returns: 
	pairs: list
		   lsit of pairs (tuples) 

	Note:
	This method is from the given file GETTING_STARTED.PDF
	If the input is [A,B,C] then the output is [(A,B),(B,C)]
	'''
	pairs = [pair for pair in zip(path[:-1], path[1:])]
	return pairs

#Function 6 for optimisation
def distance_calculator(network,pair):
	'''
	Returns distance between 2 nodes in the network 
	----------
	Parameters: 
	network: object
			 graph object contains the network 
	pair: tuple 
		  2 nodes in the network
	----------
	Returns: 
	distance: float
			  distance between 2 nodes in pair argument 
	
	Note:
	This function is made for parallelisation
	'''
	distance=nx.shortest_path_length(network,pair[0],pair[1],weight='weight')
	return distance

#Function 7
def average(network,list_nodes,how,method):
	'''
	Returns the average longitude or latitude of the nodes 
	----------
	Parameters: 
	network: object
			 Graph object contains the network
	list_nodes: list
				list of names (str) of the nodes 
	how: str
		 lgn or lat
		 lgn for the average longitude, lat for the average latitude
	method: str 
			median or mean
			median returns the median longitude/latitude, mean returns the mean longitude/latitude
	----------
	Returns: 
	average: float
			 the median or mean longitude/latitude of the nodes 
	'''
	#Initialise
	coordinate=[]

	#Loop through all nodes 
	for node in list_nodes:
		coordinate.append(network.nodes[node][how])
	
	#if mean, returns mean
	if method is 'mean':
		return np.mean(coordinate)
	else: 
		return np.median(coordinate)


#Function 8
def write_path_file(path,name):
	'''
	Create a text file contains the path
	----------
	Parameters:
	path: list
		  list of strings 
	----------
	Notes: 
	The structure of the file is 
		Node 1
		Node 2
		Node 3
		.
		.
		.
		Node N
	'''
	#Create a new file 
	fp=open(name+'.txt','w')

	#Write 
	for p in path:
		fp.write(p+'\n')

	#Close file 
	fp.close()

#Function 9
def graph(network,path,name):
	'''
	Graph the path from list of rest homes
	-----------
	Parameters: 
	network: object
			 graph object contains the network 
	path: list
		  list of names (str) which is the path
	name : str
		   name of the file  
	'''
	#Reference
	#https://piazza.com/class/k6jxvh3bhp62kk?cid=592 
	#from David Wu
	#Create list of full path (path of rest homes and numerical nodes)
	all_path_nodes = []
	# Iterating through pairs of rest homes in the path
	for rest_home_1, rest_home_2 in zip(path[:-1], path[1:]):
		path_with_nodes = nx.shortest_path(network, rest_home_1, rest_home_2, weight='weight')
		all_path_nodes.extend(path_with_nodes[:-1]) # all except the final node since this repeated on the next section
	all_path_nodes.append(path[-1])

	plot_path(network, all_path_nodes, save=name)

#Function 10
def swapnode(path,distance,matrix,full_path):
	'''
	modify the path by swapping the node's position to produce smaller (or equal) distance/cost

	----------
	Parameters: 
	path: list
		  list of names (str) of the nodes in the path 
	distance: float 
			  total distance (cost) of the path
	matrix: ndarray 
			distance matrix contains the distance between all nodes 
	full_path: list
			   list of names (str) of nodes correspond to the order of elements of matrix argument. 

	----------
	Returns: 
	distance: float
			  new distance which is smaller or equal to the distance argument 

	----------
	Notes: 
	the path is modified in place. If swapping elements produces a path with smaller distance, then the path input is destroyed. 
	matrix must be a square matrix with the following structure 
		A	B	C	...		Z
	A	0	a1	a2	...		an
	B	b0	0	b2	...		bn	
	C	b0	b1	0	...		bn
	.				.
	.					.	
	.						.
	Z	z0	z1	z2	...		0
	with full_path=[A,B,C,...,Z].
	'''

	#Initialise stopping condition, stop when no improvement is made
	noImprove=False
	while not noImprove:
		count=0 #keep track of improvement made
		j=0
		#Loop through all nodes
		while not(j==(len(path)-4)):
			#Loop through the rest of the nodes from position j+2
			for i in range(j+2,len(path)-2):
				#try swap 2 nodes 
				swap(path,j+1,i)

				#calculate total distance 
				distance_swap=total_distance(path,matrix,full_path)
				
				#If new total distance is larger then current distance, swap back 
				if distance_swap > distance:
					swap(path,j+1,i)
				#If new total distance is less than current distance, keep and change distance 
				elif distance_swap < distance: 
					distance=distance_swap
					count += 1 #Improvement +1  

			#Increment of j 
			j+=1

		#If no improvement made, stop
		if count == 0:
			noImprove=True
	
	return distance

#Function 11
def twoopt(path,distance,matrix,full_path):
	'''
	returns a new path optimised by 2 opt algorithm 
	-----------
	Parameters: 
	path: list
		  list of names (str) of the nodes in the path 
	distance: float 
			  total distance (cost) of the path
	matrix: ndarray 
			distance matrix contains the distance between all nodes 
	full_path: list
			   list of names (str) of nodes correspond to the order of elements of matrix argument. 

	----------
	Returns: 
	new_path: list
			  the new path optimised by 2 opt algorithm
	distance: float
			  new distance which is smaller or equal to the distance argument 
	
	Notes:
	matrix must be a square matrix with the following structure 
		A	B	C	...		Z
	A	0	a1	a2	...		an
	B	b0	0	b2	...		bn	
	C	b0	b1	0	...		bn
	.				.
	.					.	
	.						.
	Z	z0	z1	z2	...		0
	with full_path=[A,B,C,...,Z].
	'''

	#Create pairs from path
	pairs=pairs_generator(path)

	#Stopping condition 
	noImprove=False
	while not noImprove:

		j = 0
		count = 0 #keep track of improvement 
		while not(j==len(pairs)-4):
			#calculate the distance of the pivot pair, call it pair (1-2)
			distance_1_2 = matrix[full_path.index(pairs[j][0])][full_path.index(pairs[j][1])] 
			#loop through the rest of the pairs except the last pair 
			for i in range(j+2,len(pairs)-2):
				#distance of next pair, called pair (3,4)
				distance_3_4 = matrix[full_path.index(pairs[i][0])][full_path.index(pairs[i][1])]

				#calculate distance for pairs (1-3) and (2-4)
				distance_1_3 = matrix[full_path.index(pairs[j][0])][full_path.index(pairs[i][0])]
				distance_2_4 = matrix[full_path.index(pairs[j][1])][full_path.index(pairs[i][1])]

				#if total distance of pair 1-2 and 3-4 is larger than 1-3 and 2-4, then change 
				if (distance_1_2+distance_3_4)>(distance_1_3+distance_2_4):
					#make new tuple
					pair_1_3 = (pairs[j][0],pairs[i][0])
					pair_2_4 = (pairs[j][1],pairs[i][1])

					#remove and add new pairs into list
					pairs.remove(pairs[j])
					pairs.insert(j,pair_1_3)
					pairs.remove(pairs[i])
					pairs.insert(i,pair_2_4)

					#Reorder the path 
					new_path=redirect(pairs)

					#Reorder pairs 
					pairs=pairs_generator(new_path)

					#Update distance 
					distance -= (distance_1_2+distance_3_4)-(distance_1_3+distance_2_4)

					#Go to next pair 
					j+=1
					count +=1 #improvement made 
					break
				
				#stopping condition 
				if i==(len(pairs)-3):
					j+=1 
		
		#If no improvement is madem stop
		if count == 0:
			noImprove=True		

	#Correct the path and then return 
	new_path=redirect(pairs)
	return new_path,distance

#Function 12
def total_distance(path,matrix,full_path):
	'''
	Calculate the total distance of the path
	----------
	Parameters: 
	path: list
		  list of names (str) of the nodes in the path 
	matrix: ndarray 
			distance matrix contains the distance between all nodes 
	full_path: list
			   list of names (str) of nodes correspond to the order of elements of matrix argument.
	
	-----------
	Returns:
	total: float
		   total distance of the path 
	'''
	#Initialise 
	total=0

	#loop through pairs of the path 
	for l in range(len(path)-1):
		total += matrix[full_path.index(path[l])][full_path.index(path[l+1])] #get distance from matrix
	return total

#Function 13
def solve(network,path,matrix,full_path,name):
	'''
	optimises a given tour/path, store and graph the output
	----------
	Parameters: 
	network: object 
			 Graph object contains the network 
	path: list
		  list of names (str) of the nodes in the path 
	matrix: ndarray 
			distance matrix contains the distance between all nodes 
	full_path: list
			   list of names (str) of nodes correspond to the order of elements of matrix argument.
	name: str
		  name of the file that the outputs will be saved as
	-----------
	Note: 
	The output will be saved as 2 files. name.txt contains the path, name.png contains the graph of the path
	'''
	
	#Calculate the distance of current path 
	distance = total_distance(path,matrix,full_path)

	#Optimising by swaping the nodes  
	distance = swapnode(path,distance,matrix,full_path)

	#Optimising using 2-opt algorithm
	path,distance = twoopt(path,distance,matrix,full_path)
	
	#Create and write the output on the file 
	write_path_file(path,name)

	#Create graph of the file 
	graph(network,path,name)

#Main function 
def main():
	'''Produces 4 courier paths for vaccines delivery in Auckland from Auckland Airport
	Note: 
	the network.graphml and rest_homes.txt files must be exactly the same as the ones given
	'''
	#Get the network
	auckland = read_network('network.graphml')

	#List of destinations including Auckland Airport at the start
	rest_homes = get_rest_homes('rest_homes.txt')
	rest_homes_dis=rest_homes.copy()
	rest_homes_dis.insert(0,'Auckland Airport')

	#Produce distance matrix, if this code block is uncommented, the computation time is 12 minutes.
	#ncpus=8
	#p=Pool(ncpus)
	#dist=[]
	#for i in range(len(rest_homes_dis)):
	#	pairs=[(auckland,(rest_homes_dis[i],node)) for node in rest_homes_dis]
	#	dist.append(p.starmap(distance_calculator, pairs)) #parallelise for faster computation speed

	#Generate dist.txt file
	#fp=open('dist.txt','w')
	#for i in range(len(rest_homes_dis)):
	#	for j in range(len(rest_homes_dis)):
	#		fp.write(str(dist[i][j])+',')
	#	fp.write('\n')
	#fp.close()

	#--------------------------------------------------------------------------------------
	# If dist.txt is given and used, the computation time is about 25 seconds
	# the matrix stored in dist.txt is exactly the same as the one produced above
	# comment the line below and uncomment the block above (line 529 to 542) to see the difference in computation time.
	dist=np.genfromtxt('dist.txt',delimiter=',',usecols=np.arange(len(rest_homes_dis)))
	#--------------------------------------------------------------------------------------

	#Split east west by median
	longitude=average(auckland,rest_homes,how='lng',method='median')
	west,east=split_longitude(auckland,longitude,rest_homes)

	#split west into west_north and west_south by mean
	latitude=average(auckland,west,how='lat',method='mean')
	west_north,west_south=split_latitude(auckland,latitude,west)

	#split east into east_north and east_south by median 
	latitude=average(auckland,east,how='lat',method='median')
	east_north,east_south=split_latitude(auckland,latitude, east)

	#Modify the path 
	#All of these modifications are decided by pre-optimising the paths and observing those outputs.
	#Partioning so that all 4 paths have approximately equal distance/cost.  
	#for west south
	west_south.insert(0,'Auckland Airport') #adding Auckland Airport to the start and the end of the path
	west_south.append('Auckland Airport')
	west_south.insert(-1,"St Margaret's Hospital and Rest Home")
	west_south.remove('Hillsborough Hospital') 
	west_south.remove('Murray Halberg Retirement Village')
	west_south.remove('Gracedale Hospital')

	#For west north
	west_north.insert(0,'Auckland Airport') #adding Auckland Airport to the start and the end of the path
	west_north.append('Auckland Airport')
	west_north.remove("St Margaret's Hospital and Rest Home")
	west_north.remove("St Catherine's Rest Home")
	west_north.remove("St Joseph's Home & Hospital")
	west_north.remove('Northbridge Lifecare Trust Rest Home & Hospital')
	west_north.remove('Anne Maree Court')
	west_north.remove('Forrest Hill Home and Hospital')
	west_north.remove('Lady Allum Rest Home and Village')

	#for east north
	east_north.insert(0,'Auckland Airport') #adding Auckland Airport to the start and the end of the path
	east_north.append('Auckland Airport')
	east_north.insert(-1,"St Catherine's Rest Home")
	east_north.insert(-1,"St Joseph's Home & Hospital") 
	east_north.insert(-1,'Northbridge Lifecare Trust Rest Home & Hospital')
	east_north.insert(-1,'Anne Maree Court')
	east_north.insert(-1,'Forrest Hill Home and Hospital')
	east_north.insert(-1,'Lady Allum Rest Home and Village')

	#for south east
	east_south.insert(0,'Auckland Airport') #adding Auckland Airport to the start and the end of the path
	east_south.append('Auckland Airport')
	east_south.insert(-1,'Hillsborough Hospital') 
	east_south.insert(-1,'Murray Halberg Retirement Village')
	east_south.insert(-1,'Gracedale Hospital')

	#Solving and optimising the paths 
	solve(auckland,west_north,dist,rest_homes_dis,name='path_1')
	solve(auckland,west_south,dist,rest_homes_dis,name='path_2')
	solve(auckland,east_north,dist,rest_homes_dis,name='path_3')
	solve(auckland,east_south,dist,rest_homes_dis,name='path_4')

if __name__ == "__main__":
	main()