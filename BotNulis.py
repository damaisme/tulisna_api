
kertas = {
  1:{'path':'bahan/kertas1.jpg','px':500,'py':420,'baris':25,'perEnter':135,'header':{'px':450,'py':60,'perEnter':90},'tanggal':{'px':2330,'py':180}}, #done

  2:{'path':'bahan/kertas2.jpg','px':585,'py':390,'baris':31,'perEnter':115,'header':{'px':460,'py':90,'perEnter':70},'tanggal':{'px':2300,'py':210}}
    #done
}
font = {
  1:{'path':'bahan/font1.ttf', 'ukuran':65, 'warna':(49, 50, 50),'max':{1:86,2:80}},
  2:{'path':'bahan/font2.ttf', 'ukuran':70, 'warna':(42, 43, 43),'max':{1:97,2:92}}
}

class BotNulis:
  def __init__(self,text,indexKertas,indexFont,header,tanggal):
    self.text = text
    self.nomerKertas = indexKertas
    self.nomerFont = indexFont
    self.pkertas = kertas[indexKertas]
    self.pfont = font[indexFont]
    self.header =header
    self.tanggal = tanggal

  def start(self):
    self.kertas = Image.open(self.pkertas['path'])
    self.draw = ImageDraw.Draw(self.kertas)
    self.myfont = ImageFont.truetype(self.pfont['path'],self.pfont['ukuran'])
    return self.prosesText()

  def prosesText(self):
    splitEnter = self.text.split('\n')
    jumlahEnter = len(splitEnter)
    if jumlahEnter>self.pkertas['baris']:
      response = {'error':True,'msg':'Jumla baris berlebih, baris anda: '+str(jumlahenter)+'. Sedangkan max baris kertas ini: '+str(self.pkertas['baris'])}
      return response
    else:
      self.textPerBaris = []
      maxKarakter = self.pfont['max'][int(self.nomerKertas)]
      for baris in splitEnter:
        panjangBaris = len(baris)
        while panjangBaris>maxKarakter:
          self.textPerBaris.append(baris[:maxKarakter])
          baris = baris[maxKarakter:]
          panjangBaris-=maxKarakter
        else:
          self.textPerBaris.append(baris)

      if len(self.textPerBaris)>self.pkertas['baris']:
        return {'error':True,'msg':'Jumla baris berlebih, baris anda: '+str(jumlahenter)+'. Sedangkan max baris kertas ini: '+str(self.pkertas['baris'])}

      return self.nulis()


  def nulis(self):
    #tulis header
    if self.header != '':
      px = self.pkertas['header']['px']
      py = self.pkertas['header']['py']
      splitHeader = self.header.split('\n')
      for baris in splitHeader:
        self.draw.text((px, py), baris, font=self.myfont, fill = self.pfont['warna'])
        py += self.pkertas['header']['perEnter']

    #nulis tgl
    if self.tanggal != '':
      px = self.pkertas['tanggal']['px']
      py = self.pkertas['tanggal']['py']
      self.draw.text((px, py), self.tanggal, font=self.myfont, fill = self.pfont['warna'])

    px = self.pkertas['px']
    py = self.pkertas['py']

    for text in self.textPerBaris:
      self.draw.text((px, py), text, font=self.myfont, fill = self.pfont['warna'])
      py+=self.pkertas['perEnter']

    self.lokasi = 'hasil/'+waktuFile+'-radendi.jpg'
    self.kertas = self.kertas.resize((1560,2080))
    self.kertas.save(self.lokasi)
    return self.upload()

  def upload(self):
    url = 'https://api.imgbb.com/1/upload'
    files = {'image': open(self.lokasi, 'rb')}
    data = {
      'key':'e06797d72d41cd832478310b4f79273c'
      }
    response = requests.request('POST',url,data=data,files=files)
    result = response.json()
    self.urlResult = result['data']['url']
    os.remove(self.lokasi)
    return {'error':False,'file':self.urlResult,'msg':'semoga bermanfaat -radendi'}
