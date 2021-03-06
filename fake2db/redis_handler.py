import redis
from helpers import fake2db_logger, rnd_id_generator


logger, extra_information = fake2db_logger()
d = extra_information

try:
    from faker import Factory
except ImportError:
    logger.error('faker package not found onto python packages, please run : \
    pip install -r requirements.txt on the root of the project')


class Fake2dbRedisHandler():
    faker = Factory.create()

    def fake2db_redis_initiator(self, host, port, number_of_rows, name=None):
        '''Main handler for the operation
        '''

        client, pipe = self.database_caller_creator(host, port, name)

        self.data_filler_simple_registration(number_of_rows, pipe)
        self.data_filler_detailed_registration(number_of_rows, pipe)
        self.data_filler_company(number_of_rows, pipe)
        self.data_filler_user_agent(number_of_rows, pipe)
        self.data_filler_customer(number_of_rows, pipe)

        client.save()

    def database_caller_creator(self, host, port, name=None):
        '''creates a redis connection object
        which will be later used to modify the db
        '''

        name = name or 0
        client = redis.StrictRedis(host=host, port=port, db=name)
        pipe = client.pipeline(transaction=False)
        return client, pipe

    def data_filler_simple_registration(self, number_of_rows, pipe):
        '''creates keys with simple regis. information
        '''

        try:
            for i in range(number_of_rows):
                pipe.hmset('simple_registration:%s' % i, {
                    'id': rnd_id_generator(self),
                    'email': self.faker.safe_email(),
                    'password': self.faker.md5(raw_output=False)
                })
            pipe.execute()
            logger.warning('simple_registration Commits are successful after write job!', extra=d)

        except Exception as e:
            logger.error(e, extra=d)

    def data_filler_detailed_registration(self, number_of_rows, pipe):
        '''creates keys with detailed regis. information
        '''

        try:
            for i in range(number_of_rows):
                pipe.hmset('detailed_registration:%s' % i, {
                    'id': rnd_id_generator(self),
                    'email': self.faker.safe_email(),
                    'password': self.faker.md5(raw_output=False),
                    'lastname': self.faker.last_name(),
                    'name': self.faker.name(),
                    'address': self.faker.address(),
                    'phone': self.faker.phone_number()
                })
            pipe.execute()
            logger.warning('detailed_registration Commits are successful after write job!', extra=d)

        except Exception as e:
            logger.error(e, extra=d)

    def data_filler_user_agent(self, number_of_rows, pipe):
        '''creates keys with user agent data
        '''

        try:
            for i in range(number_of_rows):
                pipe.hmset('user_agent:%s' % i, {
                    'id': rnd_id_generator(self),
                    'ip': self.faker.ipv4(),
                    'countrycode': self.faker.country_code(),
                    'useragent': self.faker.user_agent()
                })
            pipe.execute()
            logger.warning('user_agent Commits are successful after write job!', extra=d)

        except Exception as e:
            logger.error(e, extra=d)

    def data_filler_company(self, number_of_rows, pipe):
        '''creates keys with company data
        '''

        try:
            for i in range(number_of_rows):
                pipe.hmset('company:%s' % i, {
                    'id': rnd_id_generator(self),
                    'name': self.faker.company(),
                    'date': self.faker.date(pattern="%d-%m-%Y"),
                    'email': self.faker.company_email(),
                    'domain': self.faker.safe_email(),
                    'city': self.faker.city()
                })
            pipe.execute()
            logger.warning('companies Commits are successful after write job!', extra=d)

        except Exception as e:
            logger.error(e, extra=d)

    def data_filler_customer(self, number_of_rows, pipe):
        '''creates keys with customer data
        '''

        try:
            for i in range(number_of_rows):
                pipe.hmset('customer:%s' % i, {
                    'id': rnd_id_generator(self),
                    'name': self.faker.name(),
                    'lastname': self.faker.last_name(),
                    'address': self.faker.address(),
                    'country': self.faker.country(),
                    'city': self.faker.city(),
                    'registry_date': self.faker.date(pattern="%d-%m-%Y"),
                    'birthdate': self.faker.date(pattern="%d-%m-%Y"),
                    'email': self.faker.safe_email(),
                    'phone_number': self.faker.phone_number(),
                    'locale': self.faker.locale()
                })
            pipe.execute()
            logger.warning('customer Commits are successful after write job!', extra=d)

        except Exception as e:
            logger.error(e, extra=d)
