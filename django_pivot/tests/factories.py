import factory
from factory import fuzzy


class ProviderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'testapp.Provider'

    name = factory.Faker('company')
    score = fuzzy.FuzzyChoice('ABCDEF')


class MeteoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'testapp.Meteo'

    date = factory.Faker('date')
    provider = factory.SubFactory(ProviderFactory)
    city = factory.Faker('city')
    temperature = fuzzy.FuzzyFloat(-10, 50)
    humidity = fuzzy.FuzzyInteger(0, 100)

    @classmethod
    def create_batch_provider(self, count, provider_count, **kwargs):
        meteos = []
        for _ in range(provider_count):
            provider = ProviderFactory.create()
            meteos.extend(self.create_batch(count, provider=provider, **kwargs))
        return meteos
