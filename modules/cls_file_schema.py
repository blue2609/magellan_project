from pandas_schema.validation import CustomElementValidation, MatchesPatternValidation
from pandas_schema import Column, Schema
import numpy as np

class ClsFileSchema:
	def __init__(self):
		self.__create_col_validations()

	def get_schema(self):
		schema = Schema([
			Column('EFFECTIVE DATE', self.col_EFFECTIVE_DATE_validation),
			Column('RIC', self.col_RIC_validation),
			Column('BLOOMBERG TICKER', self.col_BLOOMBERG_TICKER_validation),
			Column('ISIN', self.col_ISIN_validation),
			Column('TICKER', self.col_TICKER_validation),
			Column('GV KEY', self.col_GV_KEY_validation),
			Column('STOCK KEY', self.col_STOCK_KEY_validation),
			Column('GICS CODE', self.col_GICS_CODE_validation),
			Column('DJI INDUSTRY CODE', self.col_DJI_INDUSTRY_CODE_validation),
			Column('COUNTRY OF DOMICILE', self.col_COUNTRY_OF_DOMICILE_validation),
			Column('COUNTRY OF LISTING', self.col_COUNTRY_OF_LISTING_validation),
			Column('CURRENCY CODE', self.col_CURRENCY_CODE_validation),
			Column('LOCAL PRICE', self.col_LOCAL_PRICE_validation),
			Column('SHARES OUTSTANDING', self.col_SHARES_OUTSTANDING_validation),
			Column('IWF', self.col_IWF_validation),
			Column('INDEX SHARES', self.col_INDEX_SHARES_validation),
			Column('INDEX MARKET CAP', self.col_INDEX_MARKET_CAP_validation),
			Column('INDEX WEIGHT', self.col_INDEX_WEIGHT_validation),
			Column('DAILY PRICE RETURN', self.col_DAILY_PRICE_RETURN_validation),
			Column('DAILY TOTAL RETURN', self.col_DAILY_TOTAL_RETURN_validation),
			Column('DIVIDEND', self.col_DIVIDEND_validation),
			Column('NET DIVIDEND', self.col_NET_DIVIDEND_validation)
		])
		return schema
	
	def __check_decimal(self, value):
		try:
			float(value)
		except ValueError:
			return False
		return True

	def __check_int(self, value):
		try:
			int(value)
		except ValueError:
			return False
		return True
	
	
	def __create_col_validations(self):
		self.col_EFFECTIVE_DATE_validation = [
			MatchesPatternValidation(r'^\d{8}$'),
			CustomElementValidation(lambda value: value is not np.nan, 'this field cannot be null')	
		]
		self.col_RIC_validation = [
			MatchesPatternValidation(r'^[A-Z0-9]{3,5}\.AX$'),
			CustomElementValidation(lambda value: value is not np.nan, 'this field cannot be null')	
		]
		self.col_BLOOMBERG_TICKER_validation = [
			MatchesPatternValidation(r'^[A-Z0-9]{3,5} AT$'),
			CustomElementValidation(lambda value: value is not np.nan, 'this field cannot be null')	
		]
		self.col_ISIN_validation = [
			MatchesPatternValidation(r'^[A-Z]{2}[A-Z0-9]{10}$'),
			CustomElementValidation(lambda value: value is not np.nan, 'this field cannot be null')	
		]
		self.col_TICKER_validation = [
			MatchesPatternValidation(r'^[A-Z0-9]{3,5}$'),
			CustomElementValidation(lambda value: value is not np.nan, 'this field cannot be null')	
		]
		self.col_GV_KEY_validation = [
			MatchesPatternValidation(r'^\d{8}W$'),
			CustomElementValidation(lambda value: value is not np.nan, 'this field cannot be null')	
		]
		self.col_STOCK_KEY_validation = [
			MatchesPatternValidation(r'^\d+$'),
			CustomElementValidation(lambda value: value is not np.nan, 'this field cannot be null')	
		]
		self.col_GICS_CODE_validation = [
			MatchesPatternValidation(r'^\d{8}$'),
			CustomElementValidation(lambda value: value is not np.nan, 'this field cannot be null')	
		]
		self.col_DJI_INDUSTRY_CODE_validation = [
			MatchesPatternValidation(r'^D\d{16}$'),
			CustomElementValidation(lambda value: value is not np.nan, 'this field cannot be null')	
		]
		self.col_COUNTRY_OF_DOMICILE_validation = [
			MatchesPatternValidation(r'^([A-Z]{2}|[A-Z]{3})$'),
			CustomElementValidation(lambda value: value is not np.nan, 'this field cannot be null')	
		]
		self.col_COUNTRY_OF_LISTING_validation = [
			MatchesPatternValidation(r'^([A-Z]{2}|[A-Z]{3})$'),
			CustomElementValidation(lambda value: value is not np.nan, 'this field cannot be null')	
		]
		self.col_CURRENCY_CODE_validation = [
			MatchesPatternValidation(r'^[A-Z]{3}$'),
			CustomElementValidation(lambda value: value is not np.nan, 'this field cannot be null')	
		]
		self.col_LOCAL_PRICE_validation = [
			CustomElementValidation(lambda value: self.__check_decimal(value) or self.__check_int(value), 'is not decimal or integer'),
			CustomElementValidation(lambda value: value is not np.nan, 'this field cannot be null')	
		]
		self.col_SHARES_OUTSTANDING_validation = [
			MatchesPatternValidation(r'^\d+$'),
			CustomElementValidation(lambda value: value is not np.nan, 'this field cannot be null')	
		]
		self.col_IWF_validation = [
			CustomElementValidation(lambda value: self.__check_decimal(value) or self.__check_int(value), 'is not decimal or integer'),
			CustomElementValidation(lambda value: value is not np.nan, 'this field cannot be null')	
		]
		self.col_INDEX_SHARES_validation = [
			CustomElementValidation(lambda value: self.__check_decimal(value) or self.__check_int(value), 'is not decimal or integer'),
			CustomElementValidation(lambda value: value is not np.nan, 'this field cannot be null')	
		]
		self.col_INDEX_MARKET_CAP_validation = [
			CustomElementValidation(lambda value: self.__check_decimal(value) or self.__check_int(value), 'is not decimal or integer'),
			CustomElementValidation(lambda value: value is not np.nan, 'this field cannot be null')	
		]
		self.col_INDEX_WEIGHT_validation = [
			CustomElementValidation(lambda value: self.__check_decimal(value), 'is not decimal'),
			CustomElementValidation(lambda value: value is not np.nan, 'this field cannot be null')	
		]
		self.col_DAILY_PRICE_RETURN_validation = [
			CustomElementValidation(lambda value: self.__check_decimal(value) or self.__check_int(value), 'is not decimal or integer'),
			CustomElementValidation(lambda value: value is not np.nan, 'this field cannot be null')	
		]
		self.col_DAILY_TOTAL_RETURN_validation = [
			CustomElementValidation(lambda value: self.__check_decimal(value) or self.__check_int(value), 'is not decimal or integer'),
			CustomElementValidation(lambda value: value is not np.nan, 'this field cannot be null')	
		]
		self.col_DIVIDEND_validation = [
			CustomElementValidation(lambda value: self.__check_decimal(value), 'is not decimal'),
		]
		self.col_NET_DIVIDEND_validation = [
			CustomElementValidation(lambda value: self.__check_decimal(value), 'is not decimal'),
		]
		

