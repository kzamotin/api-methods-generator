require "net/http"
require 'json'


class Sample
    
    def initialize (uri, token, delay )
        @uri=uri
        @token=token
		@delay=delay
        @genericfilter={sortBy:'',offset:'',limit: '' }
    end
   #==============================

    def make_json(methodname, params)
        return {jsonrpc: 2.0, method: methodname, token:@token, params: params, filter: @genericfilter}.to_json
    end
    
    def make_request(json)
        uri = URI(@uri)
        http = Net::HTTP.new(uri)

        req = Net::HTTP::Post.new(uri, {'Content-Type' => 'application/json'})
        req.body = json
        
        begin
            res = Net::HTTP.start(uri.hostname, uri.port) do |http|
            http.request(req)
            end
        rescue
            abort( "Error connection to Sample client")
            return nil
        ensure
	    if res.code != 200
            return res.body
	    end
        end
    end
    #==============================
	def genericFilter(sortBy, offset, limit)
		@genericfilter={sortBy:sortBy,offset:offset,limit: limit }
	end
        
    #====================
   
    def genericFilterClear()
		@genericfilter={sortBy:'',offset:'',limit: '' }
	end
 
 	#====================  
	def get_system_info( ) 
		json=make_json('get_system_info',{

		})
		puts ('get_system_info  method call' )
		result = make_request(json)    
		return result
	end
	#====================  
	def get_status( ) 
		json=make_json('get_status',{

		})
		puts ('get_status  method call' )
		result = make_request(json)    
		return result
	end
	#====================  
	def set_status(status, mood ) 
		json=make_json('set_status',{
			'status' : status,
			'mood' : mood
		})
		puts ('set_status  method call' )
		result = make_request(json)    
		return result
	end
	#====================  
	def make_payment(from_wallet, to_wallet, amount, comment ) 
		json=make_json('make_payment',{
			'from_wallet' : from_wallet,
			'to_wallet' : to_wallet,
			'amount' : amount,
			'comment' : comment
		})
		puts ('make_payment  method call' )
		result = make_request(json)    
		return result
	end

end