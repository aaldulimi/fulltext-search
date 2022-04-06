date = '2021-01-01T10:00:07.000Z'

date.replace('.000Z', '+00:00')

print(date[:date.find('.000Z')] + '+00:00')
print(date)