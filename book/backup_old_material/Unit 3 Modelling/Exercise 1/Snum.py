def Snum( St,k,dt):
#function to calculate the numerical solution of a linear reservoir
	S=St-k*dt*St
	return(S)
