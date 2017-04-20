import pickle

if __name__ == "__main__":
    a = '/Users/fengwei/Downloads/projectCode/hed-dlg-truncated-cn-python3/Prepare_Data_CN/pkl_data/ajmd_demo_test.dict.pkl'
    a = '/Users/fengwei/Downloads/projectCode/hed-dlg-truncated-cn-python3/tests/data/MT_WordEmb.pkl'
    fr = open(a,'rb')
    inf = pickle.load(fr)
    for i in inf:
        print(i)
