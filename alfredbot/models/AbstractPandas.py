import pandas as pd
#generic Pandas model
class AbstractPandas(dict): 

	__getattr__ = dict.get
	__delattr__ = dict.__delitem__
	__setattr__ = dict.__setitem__

	#save in the database
	def save(self):
		if not self.df[self.df.id==self.id].empty:
			self.df.loc[self.df.id==self.id,self.df.columns] = [self.get(k,"") for k in self.df.columns]
		else:
			data = pd.DataFrame([[self.get(k,"") for k in self.df.columns]], columns = self.df.columns)
			self.df = self.df.append(data, ignore_index=True)
		
		self.df.to_csv(self.file,index=False)
	#load from the database
	def reload(self):
		if self.id:
			row = self.df.loc[self.df["id"]==self.id]
			if len(row)!=0:
				row = row.values[0]
				self.update({k:row[i] for i,k in enumerate(self.df.columns)})

	#remove from the database
	def remove(self):
		if self.id:
			self.df = self.df[self.df.id!=self.id]
			self.df.to_csv(self.file,index=False)
			self.load_dataframe(self.file)

	def to_dict(self):
		return {k:self.get(k,"") for k in self.df.columns}

	def to_string(self):
		return "\n".join(["{}: {}".format(p,self.get(p,"")) for p in self.df.columns])

	def load_dataframe(self,file):
		self.file = file
		self.df = pd.read_csv(file)

	def get_all(self):
		return [
				{
				p:row.values[i] for i,p in enumerate(self.df.columns)
				}
				for _,row in self.df.iterrows()
		]