import { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { toast } from "sonner";
import { authAPI } from "@/services/api";
import { useAuth } from "@/contexts/AuthContext";
import { useRecaptcha } from "@/hooks/use-recaptcha";
import { Loader2, AlertCircle } from "lucide-react";

const Login = () => {
  const navigate = useNavigate();
  const { login } = useAuth();
  const siteKey = import.meta.env.VITE_RECAPTCHA_SITE_KEY;
  const { containerRef, isVerified, initRecaptcha, getToken, resetRecaptcha } =
    useRecaptcha(siteKey);

  const [loading, setLoading] = useState(false);
  const [recaptchaError, setRecaptchaError] = useState("");
  const [formData, setFormData] = useState({
    login: "",
    password: "",
  });

  useEffect(() => {
    // Initialize reCAPTCHA when component mounts
    const timer = setTimeout(() => {
      initRecaptcha();
    }, 100);
    return () => clearTimeout(timer);
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!formData.login || !formData.password) {
      toast.error("Please fill in all fields");
      return;
    }

    if (!isVerified) {
      setRecaptchaError("Please verify that you are not a robot");
      toast.error("Please complete the reCAPTCHA verification");
      return;
    }

    const token = getToken();
    if (!token) {
      setRecaptchaError("reCAPTCHA verification failed. Please try again.");
      toast.error("reCAPTCHA verification failed. Please try again.");
      return;
    }

    setLoading(true);
    setRecaptchaError("");
    try {
      const response = await authAPI.login({
        ...formData,
        recaptcha_token: token,
      });
      const accessToken = response.access_token || response.token;
      const user = response.user;

      login(accessToken, user);
      toast.success("Welcome back!");
      resetRecaptcha();
      navigate("/chat");
    } catch (error: any) {
      toast.error(
        error.response?.data?.detail ||
          "Login failed. Please check your credentials."
      );
      resetRecaptcha();
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-background p-4">
      <Card className="w-full max-w-md shadow-lg">
        <CardHeader className="space-y-1">
          <CardTitle className="text-2xl font-bold">Welcome back</CardTitle>
          <CardDescription>Enter your credentials to continue</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="login">Username or Email</Label>
              <Input
                id="login"
                type="text"
                placeholder="username or email"
                value={formData.login}
                onChange={(e) =>
                  setFormData({ ...formData, login: e.target.value })
                }
                disabled={loading}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                type="password"
                placeholder="••••••••"
                value={formData.password}
                onChange={(e) =>
                  setFormData({ ...formData, password: e.target.value })
                }
                disabled={loading}
              />
            </div>

            {/* reCAPTCHA Widget */}
            <div className="space-y-2">
              <div ref={containerRef} className="flex justify-center" />
              {recaptchaError && (
                <div className="flex items-center gap-2 text-sm text-destructive">
                  <AlertCircle className="h-4 w-4" />
                  <span>{recaptchaError}</span>
                </div>
              )}
            </div>

            <Button
              type="submit"
              className="w-full"
              disabled={loading || !isVerified}
            >
              {loading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Signing in...
                </>
              ) : (
                "Sign in"
              )}
            </Button>
          </form>
          <div className="mt-4 text-center text-sm">
            Don't have an account?{" "}
            <Link
              to="/signup"
              className="text-primary hover:underline font-medium"
            >
              Sign up
            </Link>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Login;
