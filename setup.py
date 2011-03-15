from setuptools import setup

PACKAGE = 'nonotifytiming'

setup(
		name=PACKAGE,
		version='1.1',
		packages=[PACKAGE],
		url='http://trac-hacks.org/wiki/NoNotifyTimingPatch',
		author='Doychin Atanasov',
		long_description="""
		Makes sure you won't receive emails with empty comments for a change.
		Usually that happens when you have the worklog plugin.
		""",
		entry_points={'trac.plugins': '%s = %s' % (PACKAGE, PACKAGE)},
)
	
