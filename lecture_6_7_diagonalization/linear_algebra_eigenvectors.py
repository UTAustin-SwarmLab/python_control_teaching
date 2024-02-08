import numpy as np

def compute_and_display_eigenvals(A):

	eigenvalues, eigenvectors = np.linalg.eig(A)

	print('eigenvalues')
	print(eigenvalues)

	print(' ')
	print(' ')

	print('eigenvectors')
	print(eigenvectors)
	print(' ')
	print(' ')

if __name__ == '__main__':

	A = np.matrix([[-2, 0], [3, 1]])
	compute_and_display_eigenvals(A)

	A = np.matrix([[1, 3], [-3, 1]])
	compute_and_display_eigenvals(A)
