dashes='------------------------------------------------------------------'

def release_logic(list1,list2):

	if list1 != None:
		for item in list1:
			if item not in list2:
				list2[item] = 1
			else:
				list2[item] += 1

def videos(item1):

	viddict1 = dict()
	viddict2 = dict()

	for k in item1:
		if 'main_release' in k.data:

			if k.data['role'] == 'Main':
				for video in k.videos:
					viddict1[video.data['title']] = video.data['uri']

			else:
				for video in k.videos:
					viddict2[video.data['title']] = video.data['uri']

	return viddict1,viddict2

def output_print_genres(genres,styles,dashes):

	if len(genres) > 0 and len(styles) > 0:
		print('\n+ genres:',genres)
		print('+ styles:',styles)
		
	elif len(genres) > 0:
		print('\n+ genres:',genres)	
		print('+ no artist styles found')
			
	else:
		print('+ no artist genres found')

	print(dashes)

def output_print_videos(artist_videos,dashes):
	
	print(len(artist_videos[0]),'"MAIN" videos found')
	print(len(artist_videos[1]),'"OTHER" videos found')
	print(dashes)

def input_str(d):
	
	print(dashes)
	searchvalue = input('Enter an * Artist / Band * name: ')
	artist = d.search(searchvalue, type='artist')
	print(dashes)	
	return artist

def artists_found(artist,dashes):
	
	print('total artists found:',artist.pages)
	print(dashes)
	
def artist_iter_print(i,artist,dashes):

	print('getting data for artist:',str(i+1),'of',artist.pages)
	print(artist[i])
	print(dashes)
		
'''start discogs stuff!'''
def main():

	import discogs_client

	d = discogs_client.Client('robo167-python-data-get-testing/0.1', user_token="hVjPiReMVDhNTSKqtwLIZvfJGUggRwLlDHJulQys")

	artist = input_str(d)
	artists_found(artist, dashes)

	if artist.pages > 10:
		print('More than 10 artists found. Choose a better search term.')

	elif artist.pages > 0:
	
		for i in range(0,artist.pages):

			genres,styles, skipped, skipped_role, skipped_dupe \
			= dict(),dict(),dict(),dict(),dict()

			artist_iter_print(i, artist, dashes)
			artist_release_objects = [i for i in artist[i].releases]

			""" - Would it be better to run videos func off the all_art_rels var?
				- Get all release IDs that are main / other then get their videos
				- Then it's not querying Discogs for all the releases again
				- Instead it runs two queries later on? """

			#artist_videos = videos(artist_release_objects)
			all_artist_releases = [i.data for i in artist_release_objects]		
			print('Total releases (incl. non-master/non-artist releases)',len(all_artist_releases))
		
			for i in all_artist_releases:

				if i['type'] != 'master':
					continue
							
				elif i['role'] != 'Main':
					skipped_role[i['main_release']] = i['role']
					continue
			
				else:
					release = d.release(str(i['main_release']))
					release_logic(release.genres, genres)
					release_logic(release.styles, styles)
		
			output_print_genres(genres, styles, dashes)
			#output_print_videos(artist_videos, dashes)
			
	else:
		print('Artist not found')
		
		
if __name__ == '__main__':
	main()