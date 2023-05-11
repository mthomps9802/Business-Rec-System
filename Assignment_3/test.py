from json_parser import read_business_files
from k_medoids import k_medoids
from similarity import get_cosine_similarity


directory_path = directory = "../BusinessRec/yelp_files/business/json/"
businesses = read_business_files(directory)

# Get the clusters using the k-medoids algorithm
k = 1
def print_clusters(clusters, filename):
    with open(filename, 'w') as f:
        for i, cluster in enumerate(clusters):
            medoid = min(cluster, key=lambda b: sum(1 - get_cosine_similarity(b, other_b) for other_b in cluster))
            print(f'Cluster {i+1}:', file=f)
            print(f'Medoid: {medoid.name}', file=f)
            print('Businesses:', file=f)
            for b in cluster:
                similarity_score = round(1 - get_cosine_similarity(b, medoid), 2)
                print(f'\t- {b.name} ({b.business_id}) - Similarity Score: {similarity_score}', file=f)
            
            print(f'\nCluster {i+1}:')
            print(f'Medoid: {medoid.name}')
            print('Businesses:')
            for b in cluster:
                similarity_score = round(1 - get_cosine_similarity(b, medoid), 2)
                print(f'\t- {b.name} ({b.business_id}) - Similarity Score: {similarity_score}')
            print('\n')

        
clusters = k_medoids(businesses, k)

print_clusters(clusters, '/Users/mxrksworld/Downloads/BusinessRec/yelp_files/clusters.txt')
