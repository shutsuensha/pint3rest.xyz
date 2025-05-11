import { Logo } from "@/once-ui/components";

const person = {
  firstName: "Daniil",
  lastName: "Kupryianchyk",
  get name() {
    return `${this.firstName} ${this.lastName}`;
  },
  role: "Python Backend Developer (junior)",
  avatar: "/magic/portfolio/images/avatar.jpg",
  email: "dankupr21@gmail.com",
  location: "Europe/Minsk", // Expecting the IANA time zone identifier, e.g., 'Europe/Vienna'
  languages: ["English", "Russian"], // optional: Leave the array empty if you don't want to display languages
};

const newsletter = {
  display: false,
  title: <>Subscribe to {person.firstName}'s Newsletter</>,
  description: (
    <>
      I occasionally write about design, technology, and share thoughts on the intersection of
      creativity and engineering.
    </>
  ),
};

const social = [
  // Links are automatically displayed.
  // Import new icons in /once-ui/icons.ts
  {
    name: "GitHub",
    icon: "github",
    link: "https://github.com/shutsuensha",
  },
  {
    name: "LinkedIn",
    icon: "linkedin",
    link: "https://www.linkedin.com/in/daniil-kupryianchyk-960594322",
  },
  {
    name: "Telegram",
    icon: "telegram",
    link: "https://t.me/evalshine",
  },
  {
    name: "CV",
    icon: "document",
    link: "https://drive.google.com/file/d/1gkMx7bBNnDl95wmoXoW6aj7aF-6VDcPJ/view",
  },
  {
    name: "Email",
    icon: "email",
    link: `mailto:${person.email}`,
  },
];

const home = {
  path: "/",
  image: "",
  label: "Home",
  title: `${person.name}'s Portfolio`,
  description: `Portfolio website showcasing my work as a ${person.role}`,
  headline: <>Developing modern services with FastAPI</>,
  featured: {
    display: true,
    title: <>Recent project: <strong className="ml-4">Pinterest Clone</strong></>,
    href: "https://github.com/shutsuensha/pint3rest.xyz",
  },
  subline: (
    <>
      I'm Daniil Kupryianchyk, a Python backend developer, specializing in building fast and scalable services with FastAPI. 
      <br /> I design APIs that are both efficient and easy to maintain, always striving to improve performance and user experience.
    </>
  ),
};

const about = {
  path: "/about",
  label: "About",
  title: `About – ${person.name}`,
  description: `Meet ${person.name}, ${person.role} from ${person.location}`,
  tableOfContent: {
    display: true,
    subItems: false,
  },
  avatar: {
    display: true,
  },
  calendar: {
    display: false,
    link: "https://cal.com",
  },
  intro: {
    display: true,
    title: "Introduction",
    description: (
      <>
        A Python backend developer passionate about building high-performance APIs with FastAPI. 
        Specializing in creating scalable, secure, and efficient services, with a focus on asynchronous programming to optimize application performance.
        Expertise lies in crafting clean, reliable solutions that bridge the gap between business requirements and technical needs.
      </>
    ),
  },
  work: {
    display: true, // set to false to hide this section
    title: "Work Experience",
    experiences: [
      {
        company: "Side project - Pinterest Clone",
        timeframe: "December 2024 - Present",
        role: "Full-Stack Developer",
        achievements: [
                <>
                  Developed a Pinterest-like platform from scratch using FastAPI, Vue 3, and PostgreSQL.
                </>,
                <>
                  Implemented real-time updates and notifications using WebSockets, enhancing user experience by keeping them engaged with instant updates.
                </>,
        ],
        images: [
          // optional: leave the array empty if you don't want to display images
          {
            src: "/magic/portfolio/images/projects/project-01/welcome.png",
            alt: "Pinterest Clone - welcome",
            width: 16,
            height: 9,
          },
                    {
            src: "/magic/portfolio/images/projects/project-01/boards.png",
            alt: "Pinterest Clone - Feed",
            width: 16,
            height: 9,
          },
        ],
      },
      {
        company: "Школа программирования TeachMeSkills",
        timeframe: "сентябрь 2024- март 2025",
        role: "Python Developer (выпускник)",
        achievements: [
          <>
            Дипломный проект — разработка e-commerce платформы на Django и PostgreSQL.
          </>,
          <>
            Успешная защита дипломного проекта и получение сертификата, подтверждающего освоение принципов разработки и работы с веб-приложениями на Python.
          </>,
        ],
                images: [
          // optional: leave the array empty if you don't want to display images
          {
            src: "/magic/portfolio/images/projects/project-02/logo.png",
            alt: "Django e-commerce",
            width: 16,
            height: 9,
          },
                    {
            src: "/magic/portfolio/images/projects/project-02/TMS-1.png",
            alt: "TMS certificate",
            width: 16,
            height: 9,
          },
        ],
      },
    ],
  },
  studies: {
    display: true, // set to false to hide this section
    title: "Studies",
    institutions: [
    {
      name: "Школа программирования TeachMeSkills",
      description: <>Completed an intensive Python Developer course, focusing on backend development using FastAPI, Django, and PostgreSQL.</>,
    },
    {
      name: "Artem Shumeiko FastAPI Course",
      description: <>Completed an in-depth FastAPI course by Artem Shumeiko, which focused on building high-performance APIs with FastAPI, handling asynchronous programming, and integrating databases like PostgreSQL. The course provided hands-on experience in creating RESTful APIs, authentication systems, and deploying applications with Docker.</>,
    }
    ],
  },
  technical: {
    display: true, // set to false to hide this section
    title: "Technical skills",
    skills: [
      {
        title: "FastAPI Backend",
        description: <>Developed async RESTful APIs using FastAPI ⚡, PostgreSQL 🐘, and MongoDB 🗄️ with SQLAlchemy 🛠️ and Alembic 🏛️ for database integration and migrations. Implemented authentication with JWT + OAuth2 🔑, async communication with HTTPX 🌐 and AsyncIO 🌀, and containerization via Docker. Enabled background task processing using Celery 🐍, Celery Beat ⏱️, and RabbitMQ 🐇. Optimized caching and rate limiting using Redis 🔴, FastAPI-Cache 🧊, and FastAPI-Limiter 🛡️. Integrated email notifications with FastAPI-Mail 📧 and used Aiofiles 📂 for file handling. Built real-time features with WebSockets 🔗, SSE 📡, Redis Pub/Sub 🌀, and Redis Stream 🧭. Defined data models with Pydantic 📜, documented APIs with Strawberry GraphQL 🍓, and ensured code quality and reliability using Pytest 🧪 and Ruff 🦊, along with structured logging 📝.</>,
        // optional: leave the array empty if you don't want to display images
        images: [
          {
            src: "/magic/portfolio/images/projects/project-01/fastapi.svg",
            alt: "Project image",
            width: 9,
            height: 9,
          },
          {
            src: "/magic/portfolio/images/projects/project-01/Postgresql_elephant.svg.png",
            alt: "Project image",
            width: 9,
            height: 9,
          },
                    {
            src: "/magic/portfolio/images/projects/project-01/DOCKER.png",
            alt: "Project image",
            width: 9,
            height: 9,
          },
        ],
      },
      {
        title: "DevOps",
        description: <>Configured and deployed containerized applications using Docker 🐳 and Docker Compose 📦. Set up Nginx ⚙️ as a reverse proxy with SSL 🔒 support for secure connections. Managed CI/CD pipelines via GitLab CI/CD 🚀, deploying to VPS/VDS 🌍 environments. Integrated object storage through Yandex Cloud S3 ☁️ and OAuth2 authentication using Google Cloud ☁️. Maintained version control with Git 🌀. Implemented monitoring and observability using Prometheus 📊, Grafana 📉, Loki 📜, and Promtail 📥. Ensured error tracking and performance monitoring with Sentry 🛡️.</>,
        // optional: leave the array empty if you don't want to display images
        images: [
          {
            src: "/magic/portfolio/images/projects/devops/nginx.png",
            alt: "Project image",
            width: 9,
            height: 9,
          },
          {
            src: "/magic/portfolio/images/projects/devops/grafana.jpg",
            alt: "Project image",
            width: 9,
            height: 9,
          },
        ],
      },
      {
        title: "Vuejs Frontend",
description: <>Developed modern, responsive web applications using Vue.js 🌐 with Vue Router 🛣️ for seamless navigation and Pinia 📦 for efficient state management. Utilized Axios 📡 for API communication and styled interfaces with Tailwind CSS 💨 for a clean, utility-first design.</>
,
        // optional: leave the array empty if you don't want to display images
        images: [
          {
            src: "/magic/portfolio/images/projects/frontend/vue.png",
            alt: "Project image",
            width: 9,
            height: 9,
          },
                    {
            src: "/magic/portfolio/images/projects/frontend/pinia.svg",
            alt: "Project image",
            width: 9,
            height: 9,
          },
        ],
      },
    ],
  },
};

const blog = {
  path: "/blog",
  label: "Blog",
  title: "Writing about design and tech...",
  description: `Read what ${person.name} has been up to recently`,
  // Create new blog posts by adding a new .mdx file to app/blog/posts
  // All posts will be listed on the /blog route
};

const work = {
  path: "/work",
  label: "Work",
  title: `Projects – ${person.name}`,
  description: `Design and dev projects by ${person.name}`,
  // Create new project pages by adding a new .mdx file to app/blog/posts
  // All projects will be listed on the /home and /work routes
};

const gallery = {
  path: "/gallery",
  label: "Gallery",
  title: `Photo gallery – ${person.name}`,
  description: `A photo collection by ${person.name}`,
  // Images by https://lorant.one
  // These are placeholder images, replace with your own
  images: [
    {
      src: "/images/gallery/horizontal-1.jpg",
      alt: "image",
      orientation: "horizontal",
    },
    {
      src: "/images/gallery/horizontal-2.jpg",
      alt: "image",
      orientation: "horizontal",
    },
    {
      src: "/images/gallery/horizontal-3.jpg",
      alt: "image",
      orientation: "horizontal",
    },
    {
      src: "/images/gallery/horizontal-4.jpg",
      alt: "image",
      orientation: "horizontal",
    },
    {
      src: "/images/gallery/vertical-1.jpg",
      alt: "image",
      orientation: "vertical",
    },
    {
      src: "/images/gallery/vertical-2.jpg",
      alt: "image",
      orientation: "vertical",
    },
    {
      src: "/images/gallery/vertical-3.jpg",
      alt: "image",
      orientation: "vertical",
    },
    {
      src: "/images/gallery/vertical-4.jpg",
      alt: "image",
      orientation: "vertical",
    },
  ],
};

export { person, social, newsletter, home, about, blog, work, gallery };
