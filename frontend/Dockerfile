# Asegúrate de Node 18 en local
node -v  # 18.x

# 1) Fija path-key a CJS
npm pkg set overrides."path-key"="3.1.1"

# (opcional pero recomendable, mantenemos graceful-fs estable)
npm pkg set overrides."graceful-fs"="4.2.11"

# 2) Re-sincroniza lockfile
npm install

# 3) Verifica que quedó bien
npm ls path-key cross-spawn | grep -E "path-key|cross-spawn"

# 4) Build local (debería compilar ya)
npm run build

# 5) Sube el lockfile
git add package.json package-lock.json
git commit -m "fix(frontend): pin path-key to CJS 3.1.1 (react-scripts compat) + graceful-fs 4.2.11"
git push origin deploy-inicial