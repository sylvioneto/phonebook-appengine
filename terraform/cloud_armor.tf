resource "google_compute_security_policy" "policy" {
  provider = google-beta
  name     = "${local.application_name}-policy"

  # WAF preconfigured rules
  rule {
    action      = "deny(403)"
    priority    = "1000"
    description = "Deny SQLi sensitivity level 2"
    match {
      expr {
        expression = "evaluatePreconfiguredExpr('sqli-v33-stable', ['owasp-crs-v030301-id942251-sqli', 'owasp-crs-v030301-id942490-sqli', 'owasp-crs-v030301-id942420-sqli', 'owasp-crs-v030301-id942431-sqli', 'owasp-crs-v030301-id942460-sqli', 'owasp-crs-v030301-id942511-sqli', 'owasp-crs-v030301-id942421-sqli', 'owasp-crs-v030301-id942432-sqli'])"
      }
    }
  }

  rule {
    action      = "deny(403)"
    priority    = "1010"
    description = "Deny Cross-site scripting"
    match {
      expr {
        expression = "evaluatePreconfiguredExpr('xss-stable')"
      }
    }
  }

  rule {
    action      = "deny(403)"
    priority    = "1020"
    description = "Deny Local file inclusion"
    match {
      expr {
        expression = "evaluatePreconfiguredExpr('lfi-stable')"
      }
    }
  }

  rule {
    action      = "deny(403)"
    priority    = "1030"
    description = "Deny Remote file inclusion"
    match {
      expr {
        expression = "evaluatePreconfiguredExpr('rfi-stable')"
      }
    }
  }

  rule {
    action      = "deny(403)"
    priority    = "1040"
    description = "Deny Remote code execution"
    match {
      expr {
        expression = "evaluatePreconfiguredExpr('rce-stable')"
      }
    }
  }

  rule {
    action      = "deny(403)"
    priority    = "1050"
    description = "Deny Method enforcement (public preview)"
    match {
      expr {
        expression = "evaluatePreconfiguredExpr('methodenforcement-stable')"
      }
    }
  }

  rule {
    action      = "deny(403)"
    priority    = "1060"
    description = "Deny Scanner detection"
    match {
      expr {
        expression = "evaluatePreconfiguredExpr('scannerdetection-stable')"
      }
    }
  }

  rule {
    action      = "deny(403)"
    priority    = "1070"
    description = "Deny Protocol attack"
    match {
      expr {
        expression = "evaluatePreconfiguredExpr('protocolattack-stable')"
      }
    }
  }

  rule {
    action      = "deny(403)"
    priority    = "1080"
    description = "Deny PHP injection attack"
    match {
      expr {
        expression = "evaluatePreconfiguredExpr('php-stable')"
      }
    }
  }

  rule {
    action      = "deny(403)"
    priority    = "1090"
    description = "Deny Session fixation attack"
    match {
      expr {
        expression = "evaluatePreconfiguredExpr('sessionfixation-stable')"
      }
    }
  }

  rule {
    action      = "deny(403)"
    priority    = "1100"
    description = "Deny Newly discovered vulnerabilities"
    match {
      expr {
        expression = "evaluatePreconfiguredExpr('cve-canary')"
      }
    }
  }

  # default rule
  rule {
    action      = "allow"
    priority    = "2147483647"
    description = "default rule"
    match {
      versioned_expr = "SRC_IPS_V1"
      config {
        src_ip_ranges = ["*"]
      }
    }
  }
}
