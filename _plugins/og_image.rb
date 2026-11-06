# Point each post's social card at its generated OG image
# (assets/images/og/<slug>.png, built by `npm run og` in CI) unless the
# post sets its own `image:` in front matter.
module CmosFoundry
  class OgImage < Jekyll::Generator
    safe true
    priority :highest

    def generate(site)
      site.posts.docs.each do |post|
        next if post.data["image"]

        slug = post.basename_without_ext.sub(/\A\d{4}-\d{2}-\d{2}-/, "")
        post.data["image"] = "/assets/images/og/#{slug}.png"
      end
    end
  end
end
