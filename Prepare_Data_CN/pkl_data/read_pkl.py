import pickle

if __name__ == "__main__":
    a = '/Users/fengwei/Downloads/projectCode/hed-dlg-truncated-master/Prepare_Data_CN/pkl_data/train_demo.dict.pkl'
    # a = '/Users/fengwei/Downloads/projectCode/hed-dlg-truncated-master/Prepare_Data_CN/pkl_data/train_demo.dialogues.pkl'
    fr = open(a,'rb')
    inf = pickle.load(fr)
    for i in inf:
        print(i)