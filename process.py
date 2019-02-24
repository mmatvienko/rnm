# here to process notes and turn them into relationships
def push(triples):
    for x,y,z in triples:
        print(f'({x})-[{y}]->({z})')
