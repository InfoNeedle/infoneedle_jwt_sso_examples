# The below example expects you to have `jwt`
# in your Gemfile, you can read more about that gem at https://github.com/progrium/ruby-jwt.

require 'securerandom' unless defined?(SecureRandom)

class InfoneedleSessionController < ApplicationController
  # Configuration
  INFONEEDLE_SHARED_SECRET = ENV["INFONEEDLE_SHARED_SECRET"]
  INFONEEDLE_VENUE_ID     = ENV["INFONEEDLE_VENUE_ID"]

  def create
    if user = User.authenticate(params[:login], params[:password])
      # If the submitted credentials pass, then log user into InfoNeedle
      sign_into_infoneedle(user)
    else
      render :new, :notice => "Invalid credentials"
    end
  end

  private

  def sign_into_infoneedle(user)
    # This is the meat of the business, set up the parameters you wish
    # to forward to InfoNeedle. All parameters are documented in this page.
    iat = Time.now.to_i
    jti = "#{iat}/#{SecureRandom.hex(18)}"

    payload = JWT.encode({
      :iat   => iat, # Seconds since epoch, determine when this token is stale
      :jti   => jti, # Unique token id, helps prevent replay attacks
      :name  => user.name,
      :email => user.email,
    }, INFONEEDLE_SHARED_SECRET)

    redirect_to infoneedle_sso_url(payload)
  end

  def infoneedle_sso_url(payload)
    url = "https://www.infoneedle.com/access/#{INFONEEDLE_VENUE_ID}/jwt?jwt=#{payload}"
    url += "&return_to=#{URI.escape(params["return_to"])}" if params["return_to"].present?
    url
  end
end
