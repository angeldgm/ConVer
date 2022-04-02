import os
import threading

def defaultRun():
	fileNameExts = []
	fileNameExt = ""
	cnt = 1
	while not os.path.isfile(fileNameExt) or fileNameExts[-1] != "":
		fileNameExt = input("Introduzca el nombre y extensión del archivo "+str(cnt)+" o deje en blanco para continuar: ")
		fileNameExts.append(fileNameExt)
		if fileNameExts[-1] == "":
			break
		if not os.path.isfile(fileNameExt):
			print("No existe tal archivo. Por favor, vuelva a intentarlo.")
			cnt -= 1
		cnt += 1
	fileNameExts.remove("")
	for fileNameExt in fileNameExts:
		folder = 'Versiones_anteriores_de_'+fileNameExt
		threading.Thread(target=notFirstRun, args=(fileNameExt, folder)).start() if os.path.isdir(folder) else threading.Thread(target=firstRun, args=(fileNameExt, folder)).start()

def firstRun(fileNameExt, folder):
	if not os.path.isdir(folder):
		os.system('mkdir "Versiones_anteriores_de_'+fileNameExt)
	version = 1
	createCopyVersion(fileNameExt, version)
	print("Versión", version, "guardada")
	notFirstRun(fileNameExt, folder)

def notFirstRun(fileNameExt, folder):
	version = len([name for name in os.listdir(folder) if os.path.isfile(os.path.join(folder, name))])
	lastModified = getLastModified(fileNameExt)
	print("Okay, a la espera de cambios en el archivo "+fileNameExt)
	while True:
		lastModified2 = getLastModified(fileNameExt)
		if lastModified != lastModified2:
			lastModified = lastModified2
			version += 1
			createCopyVersion(fileNameExt, version)
			print("["+fileNameExt+"] Versión", version, "guardada")
		else:
			continue

def createCopyVersion(fileNameExt, version):
	fileName = fileNameExt.split(".")[0]
	fileExt = fileNameExt.split(".")[1]
	os.system('copy '+fileNameExt+' "Versiones_anteriores_de_'+fileNameExt+'/'+fileName+'_v'+str(version)+'.'+fileExt)

def getLastModified(fileNameExt):
	fileStatsObj = os.stat(fileNameExt)
	modificationTime = fileStatsObj[8]
	return modificationTime

if __name__ == '__main__':
	defaultRun()