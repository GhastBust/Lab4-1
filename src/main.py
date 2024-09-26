from const import *
import extract_data
from my_file import myFile
from process_data import processs


def main():

    data_files : list[myFile] = extract_data.extract()
    
    # y1, y2 = data_files[0].ch1, data_files[0].ch2
    
    processs(data_files)
    
        # print(detect_downward_curve(y1))
    
    # plt.plot(y1)
    # plt.show()
    
    
    
    
    
    ...



if __name__ == "__main__":
    main()