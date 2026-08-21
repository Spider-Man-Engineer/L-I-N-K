class Link < Formula
  desc "Live Instant Network Kommunication — terminal chat with room invite codes"
  homepage "https://github.com/SyntaxSlayerr/L-I-N-K"
  url "https://github.com/SyntaxSlayerr/L-I-N-K/archive/refs/tags/v0.1.0.tar.gz"
  sha256 "PLACEHOLDER"
  license "MIT"

  def install
    libexec.install "lnk", "server.py", "client.py"
    bin.install_symlink libexec/"lnk"
  end

  test do
    assert_match "Usage:", shell_output("#{bin}/lnk help", 0)
  end
end
