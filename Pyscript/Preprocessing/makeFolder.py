import os

def makeProjectFolder():
    projectFolder = r'C:\Final_Project_Files'
    
    # Final_Project_Files 생성
    if not os.path.exists(projectFolder):
        os.mkdir(projectFolder)

    dataesFolder = os.path.join(projectFolder, 'dataes')
    
    if not os.path.exists(dataesFolder):
        os.mkdir(dataesFolder)

        needFolder = [os.path.join(dataesFolder, 'Cosmetic', 'Final'), 
                      os.path.join(dataesFolder, 'Cosmetic', 'tempData'),
                      os.path.join(dataesFolder, 'Ingredient')]
        
        for need in needFolder:
            try:
                os.makedirs(need)
            except FileExistsError:
                pass
            
    print("Make project Folder Done")
    
if __name__ == "__main__":
    makeProjectFolder()