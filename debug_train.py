import pickle
import sys
sys.path.insert(0, '.')

print("Loading train.pkl...")
with open('train.pkl', 'rb') as f:
    train = pickle.load(f)

print(f'Type: {type(train)}')
print(f'Length: {len(train)}')

if len(train) > 0:
    print(f'\nFirst item: {train[0]}')
    print(f'First item type: {type(train[0])}')
    print(f'First item __dict__: {vars(train[0])}')
    
    # Check if it has a prompt attribute
    if hasattr(train[0], 'prompt'):
        print(f'\nFirst item prompt: {train[0].prompt}')
    else:
        print('\nFirst item has no prompt attribute')
        print(f'Available attributes: {dir(train[0])}')

