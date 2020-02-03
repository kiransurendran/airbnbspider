# -*- coding: utf-8 -*-
import scrapy
from scrapy.exceptions import CloseSpider
import json

class AirbnbSpiderSpider(scrapy.Spider):
    name = 'airbnb_spider'
    allowed_domains = ['www.airbnb.com']
    
    def start_requests(self):
         yield scrapy.Request(url='https://www.airbnb.com/api/v2/explore_tabs?_format=for_explore_search_web&auto_ib=true&client_session_id=a197a982-35ea-4ee5-a0b3-a4035ed61eae&currency=INR&current_tab_id=home_tab&experiences_per_grid=20&federated_search_session_id=56bb3645-2926-4140-944f-f701485f0012&fetch_filters=true&guidebooks_per_grid=20&has_zero_guest_treatment=true&hide_dates_and_guests_filters=false&is_guided_search=true&is_new_cards_experiment=true&is_standard_search=true&items_offset=18&items_per_grid=18&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&last_search_session_id=b3623efe-94af-4d13-b42e-27c6e40ee3d7&locale=en&map_toggle=false&metadata_only=false&place_id=ChIJOwg_06VPwokRYv534QaPC8g&query={0}&query_understanding_enabled=true&refinement_paths%5B%5D=%2Fhomes&s_tag=8d2-RBZk&satori_version=1.2.5&screen_height=884&screen_size=large&screen_width=1920&search_type=unknown&section_offset=4&selected_tab_id=home_tab&show_groupings=true&source=mc_search_bar&supports_for_you_v3=true&tab_id=home_tab&timezone_offset=330&version=1.7.3'.format(self.city),callback=self.parse_id)

    def parse_id(self,response):
        data = json.loads(response.body)
        d =  json.loads(response.body)
        # with open('next_page_data.json','a') as file:
        #     file.write(json.dumps(d))
        restaurants = data.get('explore_tabs')[0].get('sections')[0].get('listings')  
        if restaurants is None:
            raise CloseSpider("no restaurants in the city")
        
        for restaurant in restaurants:
            id = restaurant.get('listing').get('id')
            yield scrapy.Request(url='https://www.airbnb.com/api/v2/pdp_listing_details/{0}?_format=for_rooms_show&_p3_impression_id=p3_1580496964_USvnjuM8liOA9Kmq&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&'.format(id),callback= self.parse)
            #https://www.airbnb.com/api/v2/pdp_listing_details/5567361?_format=for_rooms_show&_p3_impression_id=p3_1580502540_OZ4XKfVxaM4NupGt&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&
           

        pagination_metadata = data.get('explore_tabs')[0].get('pagination_metadata')

        if pagination_metadata.get('has_next_page'):
            items_offset = pagination_metadata.get('items_offset')
            section_offset = pagination_metadata.get('section_offset')
            yield scrapy.Request(url='https://www.airbnb.com/api/v2/explore_tabs?_format=for_explore_search_web&auto_ib=true&client_session_id=a197a982-35ea-4ee5-a0b3-a4035ed61eae&currency=INR&current_tab_id=home_tab&experiences_per_grid=20&federated_search_session_id=56bb3645-2926-4140-944f-f701485f0012&fetch_filters=true&guidebooks_per_grid=20&has_zero_guest_treatment=true&hide_dates_and_guests_filters=false&is_guided_search=true&is_new_cards_experiment=true&is_standard_search=true&items_offset={0}&items_per_grid=18&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=en&map_toggle=false&metadata_only=false&place_id=ChIJOwg_06VPwokRYv534QaPC8g&query={2}&query_understanding_enabled=true&refinement_paths%5B%5D=%2Fhomes&s_tag=8d2-RBZk&satori_version=1.2.5&screen_height=884&screen_size=large&screen_width=1920&search_type=unknown&section_offset={1}&selected_tab_id=home_tab&show_groupings=true&source=mc_search_bar&supports_for_you_v3=true&tab_id=home_tab&timezone_offset=330&version=1.7.3'.format(items_offset,section_offset,self.city),callback=self.parse_id)
            # with open('next_page_json.json','w') as f:
            #     d = json.loads(response.body)
            #     f.write(json.dumps(d))
   
    # pagination is not working properly cos the link to individual pages are diff for each one.

    def parse(self, response):
        restaurant = json.loads(response.body)
        #print(restaurant)
        # with open('restaurant_details.json','w') as f:
        #     f.write(json.dumps(restaurant))
        yield{
            'id': restaurant.get('pdp_listing_detail').get('id'),
            'title':restaurant.get('pdp_listing_detail').get('name'),
            'url': restaurant.get('pdp_listing_detail').get('seo_features').get('canonical_url'),
            #'type': restaurant.get('kicker_content'),
            #'description': restaurant.get('primary_host').get('about'),
            'loation': {
                #'city': estaurant.get('pdp_listing_detail').get(''),
                'latitude': restaurant.get('pdp_listing_detail').get('lat'),
                'longitude':restaurant.get('pdp_listing_detail').get('lng')
            }
        }
 
